import json
import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from flask_cors import CORS

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  load_dotenv()
  app.config.from_mapping(
    SECRET_KEY='dev',
    CONNECTION_STRING=os.environ['SCRAPER_APP_CONNECTION_STRING'],
    OPENAI_API_KEY=os.environ['OPENAI_API_KEY']
  )
  CORS(app)

  if test_config is None:
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)
  else:
    # load the test config if passed in
    app.config.from_mapping(test_config)
  
  # ensure the instance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  from . import db
  db.init_app(app)

  from . import scraper

  @app.get("/url")
  def scrape():
    site_content = scraper.req()
    return site_content

  @app.post("/answer")
  def answer():
    print(request.json)
    try:
      client = db.connect_db()
      collection = client["site_user_survey"]["user_answers"]
      res = collection.insert_one(request.get_json())
      if not res.acknowledged:
        raise Exception("Couldn't insert data: ", request.get_json())
      client.close()

      return { 'id': str(res.inserted_id) }

    except Exception as e:
      print("Error saving answer: ", e)
      client.close()

  @app.post("/categorize")
  def categorize():
    from . import chatbot
    llm = chatbot.connect_ai()
    messages = [
      (
        "system", "The user has answered some questions about why they are visiting a website."
      ),
      (
        "system", "Categorize the user based on intent. Answer in one word."
      ),
      (
        "user", json.dumps(request.json)
      )
    ]
    category = llm.invoke(messages)

    # TODO get llm to return enum
    return jsonify(category.content)

  return app
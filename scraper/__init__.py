import os
from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  load_dotenv()
  app.config.from_mapping(
    SECRET_KEY='dev',
    CONNECTION_STRING=os.environ['SCRAPER_APP_CONNECTION_STRING'],
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
  # a simple page that says hello
  @app.route('/hello')
  def hello():
    return 'Hello, World'
  
  @app.get('/')
  def home():
    client = db.connect_db()
    names = client.list_database_names()
    return ','.join(names)

  return app
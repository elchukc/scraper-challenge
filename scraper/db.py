from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import current_app, g

def connect_db():
    try:
        # Create a new client and connect to the server
        if 'db' not in g:
            client = MongoClient(current_app.config['CONNECTION_STRING'], server_api=ServerApi('1'))
            result = client.admin.command('ping')

            if int(result.get('ok')) == 1:
                print("Connected to db.")
            else:
                raise Exception("Cluster ping returned OK != 1")

            g.db = client
        return g.db

    except Exception as e:
        print(e)


def close_db(e = None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)



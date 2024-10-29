from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()
uri = os.environ['SCRAPER_APP_CONNECTION_STRING']

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    db = client['sample_mflix']
    collections = db.list_collection_names() # ['movies', 'sessions', 'theaters', 'users', 'embedded_movies', 'comments']
    print(collections)
    movies = db.get_collection('movies')
    print(movies, '\n')
    client.close()
except Exception as e:
    print(e)
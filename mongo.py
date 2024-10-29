from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()
uri = os.environ['SCRAPER_APP_CONNECTION_STRING']

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    for db_info in client.list_database_names():
        print(db_info)
    client.close()
except Exception as e:
    print(e)
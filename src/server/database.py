from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

def get_database():
   connection_string = os.getenv('MONGODB_CONNECTION_STRING')
   try:
      client = MongoClient(connection_string, server_api=ServerApi('1'))
   except Exception:
      print("Error connecting to MongoClient")
      return None
   return client

if __name__ == "__main__":
    get_database()
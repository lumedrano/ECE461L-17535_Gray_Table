#Kimberly & Luigi

#using MongoDB through python
from pymongo import MongoClient
from dotenv import load_dotenv
import os


#for reference
'''
Structure of User entry:
User = {
    'username': username,
    'userId': userId,
    'password': password,
    'projects': [project1_ID, project2_ID, ...]
}
'''

load_dotenv()

connection_string = os.getenv('MONGODB_CONNECTION_STRING')

client = MongoClient(connection_string)

# Access a database
db = client['ece461l_final_project']

# Access a collection
collection = db['usersDB']


# Function to add a new user
def addUser(client, username, userId, password):
    # Add a new user to the database
    pass

# Helper function to query a user by username and userId
def __queryUser(client, username, userId):
    # Query and return a user from the database
    pass

# Function to log in a user
def login(client, username, userId, password):
    # Authenticate a user and return login status
    pass

# Function to add a user to a project
def joinProject(client, userId, projectId):
    # Add a user to a specified project
    pass

# Function to get the list of projects for a user
def getUserProjectsList(client, userId):
    # Get and return the list of projects a user is part of
    pass
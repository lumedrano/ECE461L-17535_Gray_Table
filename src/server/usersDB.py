#Kimberly & Luigi

#using MongoDB through python
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import cipher


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
#TODO: test and check with Kimberly
def login(username, userId, password):

    #find person using query function from above
    user = __queryUser(username, userId)
    #check if user is found, if so then use decrypt function on password by passing password in
    if user:
        encrypted_pw = user['password']
        decrypted_pw = cipher.decrypt(encrypted_pw, 3, -1)
        
        #if match then return something that they are logged in
        if decrypted_pw == password:
            return "Login Successful!"
        #if not, return error message saying invalid 
        return "Invalid password."
    #if user was not found by username/id then return user not found
    return "User not found."

# Function to add a user to a project
def joinProject(userId, projectId):
    # Add a user to a specified project

    #find userID, if found then continue to check for projectID
    
    #if projectID is found then add projectID to user's project list
    pass

# Function to get the list of projects for a user
def getUserProjectsList(client, userId):
    # Get and return the list of projects a user is part of

    #find user in db
    #if found then return their list of projects(maybe a for loop)
    pass
# Import necessary libraries and modules
import pymongo
from pymongo import MongoClient

import hardwareDB
# from src.server.hardwareDB import database, collection, client
import usersDB
import hardwareDB


'''
Structure of Project entry:
Project = {
    'projectName': projectName,
    'projectId': projectId,
    'description': description,
    'hwSets': {HW1: 0, HW2: 10, ...},
    'users': [user1, user2, ...]
}
'''

# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client['projects']
# collection  = db['projects']
# Function to query a project by its ID
def queryProject(db, projectId):
    # Query and return a project from the database
    collection = db['projectsDB']
    return collection.find_one({'projectId': projectId})
    # pass

# Function to create a new project
def createProject(db, projectName, projectId, description):
    # Create a new project in the database
    try:
        collection = db['projectsDB']
        print("collection created")
        new_project = {
            'projectName': projectName,
            'projectId': projectId,
            'description': description,
            'hwSets': {},
            'users': []
        }
        print("project created")
        collection.insert_one(new_project)
        print("project inserted")
        return "project created successfully"
    except Exception as e:
        return "project creation error: " + str(e)
    # pass

# Function to add a user to a project
def addUser(db, projectId, userId):
    # Add a user to the specified project
    collection = db['projectsDB']
    project = collection.find_one({'projectId': projectId})
    if project is None:
        return "project not found"
    project['users'].append(userId)
    return "user added successfully"
    # pass

# Function to update hardware usage in a project
def updateUsage(db, projectId, hwSetName):
    # Update the usage of a hardware set in the specified project
    collection = db['projectsDB']
    project = collection.find_one({'projectId': projectId})
    if project is None:
        return "project not found"
    project['hwSets'].update([hwSetName])

    pass

# Function to check out hardware for a project
def checkOutHW(db, projectId, hwSetName, qty, userId):
    # Check out hardware for the specified project and update availability
    # collection = db['usersDB']
    # user = collection.find_one({'userId': userId})
    # project = user['projects'].find_one({'projectId': projectId})
    # if project is None:
    #     return "project not found"
    # project['hwSets'].update([hwSetName])

    pass

# Function to check in hardware for a project
def checkInHW(client, projectId, hwSetName, qty, userId):
    # Check in hardware for the specified project and update availability
    pass

# Testing
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client['projects']
# print("client and db created")
# col = db['projects']
# new_project = {
#     'projectName': 'test',
#     'projectId': 'test',
#     'description': 'test',
#     'hwSets': {},
#     'users': []
# }
# print("project created")
# col.insert_one(new_project)
# print("project inserted")
# print(createProject(db, "myProject", "Project1", "Sample"))
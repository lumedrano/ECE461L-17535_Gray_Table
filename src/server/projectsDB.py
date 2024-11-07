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
    try:
        return collection.find_one({'projectId': projectId})
    except Exception as e:
        print(f"An error occurred while querying project: {str(e)}")
        return None
    # pass

# Function to create a new project
def createProject(db, projectName, projectId, description, userId):
    
    #TODO: when further implementing, check if we need to keep IDs in integer or if they can be mix type
    projectId = str(projectId)
    userId = str(userId)
    try:
        projects_collection = db['projectsDB']
        users_collection = db['usersDB']
        
        # checking if project already exists
        if projects_collection.find_one({'projectId': projectId}):
            return "Error: Project with this ID already exists"
        
        #check if user exists
        user = users_collection.find_one({'userId': userId})
        if not user:
            return "Error: User not found"
            
        #create the document
        new_project = {
            'projectName': projectName,
            'projectId': projectId,
            'description': description,
            'hwSets': {},
            'users': [userId]  # Add creating user to the project
        }
        
        projects_collection.insert_one(new_project)
        
        #add project to user's profile in usersDB
        users_collection.update_one(
            {'userId': userId},
            {'$push': {'projects': projectId}}
        )
        
        return "Project created successfully"
        
    except Exception as e:
        return f"Project creation error: {str(e)}"

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
    collection = db['projectsDB']
    project = collection.find_one({'projectId': projectId})
    
    if not project:
        return "Project not found."

    current_qty = project['hwSets'].get(hwSetName, 0)
    
    if current_qty < qty:
        return f"Not enough of {hwSetName} is available. Only {current_qty} is available."
    
    new_qty = current_qty - qty
    collection.update_one(
        {'projectId': projectId},
        {'$set': {f'hwSets.{hwSetName}': new_qty}}
    )

    hardwareDB.checkOut(db, hwSetName, qty)
    
    return f"{qty} of {hwSetName} checked out from project {projectId} by user {userId}."
    #pass

# Function to check in hardware for a project
def checkInHW(db, projectId, hwSetName, qty, userId):
    # Check in hardware for the specified project and update availability
    collection = db['projectsDB']
    project = collection.find_one({'projectId': projectId})
    
    if not project:
        return f"Project {projectId} not found."

    current_qty = project['hwSets'].get(hwSetName, 0)
    new_qty = current_qty + qty

    collection.update_one(
        {'projectId': projectId},
        {'$set': {f'hwSets.{hwSetName}': new_qty}}
    )

    hardwareDB.checkIn(db, hwSetName, qty)
    return f"{qty} of {hwSetName} checked in to project {projectId} by user {userId}."
    #pass
# Function to get project information

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
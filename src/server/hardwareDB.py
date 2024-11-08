# Import necessary libraries and modules
from dataclasses import dataclass
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId


'''
Structure of Hardware Set entry:
HardwareSet = {
    'hwName': hwSetName,
    'capacity': initCapacity,
    'availability': initCapacity
}
'''

# Function to create a new hardware set
#@app.route("/create_hardware_set")
# def createHardwareSet(db, hwSetName, initCapacity):
#     # Create a new hardware set in the database
#     HardwareSet = {
#         'hwName': hwSetName,
#         'capacity': initCapacity,
#         'availability': initCapacity
#     }
#     db['hardware_sets'].insert_one(HardwareSet)
#     return "Hardware Set Created Successfully"

def createHardwareSet(db, hwSetName, initCapacity, projectId):
#TODO: check to see if already exists before creating another????
    hw_collection = db['hardware_sets']
    projects_collection = db['projectsDB']
    # Create a new hardware set in the database
    HardwareSet = {
        'hwName': hwSetName,
        'capacity': initCapacity,
        'availability': initCapacity
    }
    
    # Insert the new hardware set and get the inserted ID
    result = hw_collection.insert_one(HardwareSet)
    hardware_set_id = result.inserted_id

    # Update the specified project in ProjectsDB with the new hardware set ID
    projects_collection.update_one(
        { 'projectId': projectId },  # Use projectId to find the specific project
        { '$push': { 'hwSets': hardware_set_id } }
    )
    return "Hardware Set Created Successfully"


def fetchHardwareSets(db, projectID):
    projectID = str(projectID)
    # Step 1: Find the project document by projectID
    project = db['projectsDB'].find_one({'projectId': projectID})
    
    if not project:
        return "Project not found"
    
    # Step 2: Retrieve the list of hardware set IDs from the project document
    hardware_set_ids = project.get('hwSets', [])
    
    # Step 3: Fetch the hardware set documents that match these IDs
    hardware_sets = list(db['hardware_sets'].find({'_id': {'$in': hardware_set_ids}}))
    
    # Convert ObjectId fields to strings
    for hardware_set in hardware_sets:
        hardware_set['_id'] = str(hardware_set['_id'])
    
    return hardware_sets


# Function to query a hardware set by its name
def queryHardwareSet(db, hwSetName):
    # Query and return a hardware set from the database
    return db['hardware_sets'].find_one({'hwName': hwSetName})


# Function to update the availability of a hardware set
def updateAvailability(db, hwSetName, newAvailability):
    # Update the availability of an existing hardware set
    db['hardware_sets'].update_one(
        {'hwName': hwSetName},
        {'$set': {'availability': newAvailability}}
    )
    return "Availability Updated Successfully"

# Function to request space from a hardware set
def checkOut(db, hwSetName, amount):
    # Request a certain amount of hardware and update availability
    hardware_set = queryHardwareSet(db, hwSetName)
    if hardware_set and hardware_set['availability'] >= amount:
        db['hardware_sets'].update_one(
            {'hwName': hwSetName},
            {'$inc': {'availability': -amount}}
        )
        return "Space Requested Successfully"
    return "Not Enough Availability or Hardware Set Not Found"

# Function to get all hardware set names
def getAllHwNames(db):
    # Get and return a list of all hardware set names
    setNames = db['hardware_sets'].find({}, {'hwName': 1, "_id": 0})
    return [hw['hwName'] for hw in setNames]

def checkIn(db, hwSetName, amount):
    hardware_set = queryHardwareSet(db, hwSetName)
    if hardware_set and hardware_set['capacity'] <= amount + hardware_set['availability']:
        db['hardware_sets'].update_one(
            {'hwName': hwSetName},
            {'$inc': {'availability': +amount}}
        )
        return "Checkin Successful"
    return "Checkin Failed"

# test code
# if __name__ == '__main__':
#     createHardwareSet(client, 'test', 100)
#     print(queryHardwareSet(client, 'test'))


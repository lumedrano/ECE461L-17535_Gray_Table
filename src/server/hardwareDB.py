# Import necessary libraries and modules
from dataclasses import dataclass
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

# print("PyMongo version:", pymongo.__version__)


'''
Structure of Hardware Set entry:
HardwareSet = {
    'hwName': hwSetName,
    'capacity': initCapacity,
    'availability': initCapacity
}
'''
client = MongoClient(os.getenv("MONGODB_CONNECTION_STRING"))
db = client['hardwareDB_TEST']

# Function to create a new hardware set
def createHardwareSet(db, hwSetName, initCapacity, projectId):
    hwCollection = db['hardwareSets']
    projectCollection = db['projectsDB']

    # Create a new hardware set in the database
    if(queryHardwareSet(db, hwSetName)):
        # Don't create new hardware set under existing set name
        return "A hardware set under that name already exists"

    HardwareSet = {
    'hwName': hwSetName,
    'capacity': initCapacity,
    'availability': initCapacity
    }

    try:
        result = hwCollection.insert_one(HardwareSet)
        hardwareSetID = result.inserted_id

        projectCollection.update_one(
            {'projectId': projectId},
            {'$push': {'hwSets': hardwareSetID}}
        )
        return {"message": f"Hardware Set '{hwSetName}' Created Successfully", "status": "success",
                "id": str(hardwareSetID)}
    except Exception as e:
        return {"message": f"An error occurred: {str(e)}", "status": "error"}


def deleteHardwareSet(db, hwSetName, projectId):
    hwCollection = db['hardwareSets']
    projectCollection = db['projectsDB']


    existingHardwareSet = hwCollection.find_one({'hwName': hwSetName})  # Use 'hwCollection' here
    if not existingHardwareSet:
        return "A hardware set under that name doesn't exist"


    # Get the hardware set's ID
    hardwareSetId = existingHardwareSet['_id']

    try:
        #Delete the hardware set from the hardware_sets collection
        hwCollection.delete_one({'_id': hardwareSetId})

        # Remove the hardware set ID from the project's hwSets array
        projectCollection.update_one(
            {'projectId': projectId},
            {'$pull': {'hwSets': hardwareSetId}}
        )
        return f"Hardware Set '{hwSetName}' Deleted Successfully"

    except Exception as e:
        return f"An error occurred while deleting the hardware set: {str(e)}"


def fetchHardwareSets(db, projectID):
    projectID = str(projectID)

    # Step 1: Find the project document by projectID
    project = db['projectsDB'].find_one({'projectId': projectID})

    if not project:
        return "Project not found"

    # Step 2: Retrieve the list of hardware set IDs from the project document
    hardware_set_ids = project.get('hwSets', [])

    # Step 3: If the hardware_set_ids list is empty, return an empty list
    if not hardware_set_ids:
        return []

    # Step 4: Fetch the hardware set documents that match these IDs
    hardware_sets = list(db['hardwareSets'].find({'_id': {'$in': hardware_set_ids}}))

    # Convert ObjectId fields to strings
    for hardware_set in hardware_sets:
        hardware_set['_id'] = str(hardware_set['_id'])

    return hardware_sets


# Function to query a hardware set by its name
def queryHardwareSet(db, hwSetName):
    # Query and return a hardware set from the database
    return db['hardwareSets'].find_one({'hwName': hwSetName})

# Function to update the availability of a hardware set
def updateAvailability(db, hwSetName, changeInAvailability):
    collection = db['hardwareSets']
    # Update the availability of an existing hardware set
    collection.update_one(
        {'hwName': hwSetName},
        {'$inc': {'availability': changeInAvailability}}
    )
    return "Availability Updated Successfully"

# Function to request space from a hardware set
def requestSpace(db, hwSetName, amount):
    # Request a certain amount of hardware and update availability
    # Check if the requested amount is valid (positive whole number)
    if amount <= 0 or not isinstance(amount, int):
        return {"message": "Amount must be a positive whole number", "availability": None}

    # Find the hardware set and ensure availability for the requested checkout amount
    collection = db['hardwareSets']
    hardwareSet = queryHardwareSet(db, hwSetName)
    if not hardwareSet:
        return {"message": "Hardware Set Not Found", "availability": None}

    if hardwareSet['availability'] >= amount:
        # Perform the checkout operation and retrieve the new availability
        db['hardwareSets'].update_one(
            {'hwName': hwSetName},
            {'$inc': {'availability': -amount}}
        )
        # Fetch the updated availability to return it
        newAvailability = hardwareSet['availability'] - amount
        return {"message": "Check Out Successful!", "availability": newAvailability}
    else:
        return {"message": "Not Enough Availability", "availability": hardwareSet['availability']}

# Function to get all hardware set names
def getAllHWSets(db):
    collection = db['hardwareSets']
    # Get and return a list of all hardware sets
    HWsets = collection.find({}, {'hwName': 1, 'capacity': 1, 'availability': 1, '_id': 0})
    setsList = list(HWsets)
    return setsList

# # test code
# if __name__ == '__main__':
#     collection = db['hardwareSets']
#     # Clear collection at start
#     collection.delete_many({})
#     print(createHardwareSet(db, 'test', 100))
#     print(createHardwareSet(db, 'dog', 200))
#     print(createHardwareSet(db, 'test', 200))
#     print(queryHardwareSet(db, 'test'))
#     print(requestSpace(db, 'test', 50))
#     print(updateAvailability(db, 'test', -20))
#     print(queryHardwareSet(db, 'test'))
#     setsList = getAllHWSets(db)
#     print("Listing all HWSets: ")
#     for i in setsList:
#         print(i)

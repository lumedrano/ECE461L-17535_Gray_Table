# Import necessary libraries and modules
from dataclasses import dataclass
from flask import Flask, request, jsonify
from pymongo import MongoClient

# print("PyMongo version:", pymongo.__version__)


'''
Structure of Hardware Set entry:
HardwareSet = {
    'hwName': hwSetName,
    'capacity': initCapacity,
    'availability': initCapacity
}
'''
client = MongoClient("mongodb+srv://teamAuth:QsbCrYdZbBIqDko8@ece461l.ezc85.mongodb.net/?retryWrites=true&w=majority&appName=ECE461L")
db = client['hardwareDB_TEST']

# Function to create a new hardware set
def createHardwareSet(db, hwSetName, initCapacity):
    collection = db['hardwareSets']
    # Create a new hardware set in the database
    if(queryHardwareSet(db, hwSetName)):
        # Don't create new hardware set under existing set name
        return "A hardware set under that name already exists"
    HardwareSet = {
    'hwName': hwSetName,
    'capacity': initCapacity,
    'availability': initCapacity
    }
    collection.insert_one(HardwareSet)
    return "Hardware Set Created Successfully"

# Function to query a hardware set by its name
def queryHardwareSet(db, hwSetName):
    collection = db['hardwareSets']
    # Query and return a hardware set from the database
    return collection.find_one({'hwName': hwSetName})

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
    collection = db['hardwareSets']
    # Request a certain amount of hardware and update availability
    hardware_set = queryHardwareSet(db, hwSetName)
    if hardware_set and hardware_set['availability'] >= amount:
        collection.update_one(
            {'hwName': hwSetName},
            {'$inc': {'availability': -amount}}
        )
        return "Space Requested Successfully"
    return "Not Enough Availability or Hardware Set Not Found"

# Function to get all hardware set names
def getAllHWSets(db):
    collection = db['hardwareSets']
    # Get and return a list of all hardware sets
    HWsets = collection.find({}, {'hwName': 1, 'capacity': 1, 'availability': 1, '_id': 0})
    setsList = list(HWsets)
    return setsList

# test code
if __name__ == '__main__':
    collection = db['hardwareSets']
    # # Clear collection at start
    # collection.delete_many({})
    print(createHardwareSet(db, 'test', 100))
    print(createHardwareSet(db, 'dog', 200))
    print(createHardwareSet(db, 'test', 200))
    print(queryHardwareSet(db, 'test'))
    print(requestSpace(db, 'test', 50))
    print(updateAvailability(db, 'test', -20))
    print(queryHardwareSet(db, 'test'))
    setsList = getAllHWSets(db)
    print("Listing all HWSets: ")
    for i in setsList:
        print(i)


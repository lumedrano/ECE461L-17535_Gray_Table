# Import necessary libraries and modules
from dataclasses import dataclass

from pymongo import MongoClient

'''
Structure of Hardware Set entry:
HardwareSet = {
    'hwName': hwSetName,
    'capacity': initCapacity,
    'availability': initCapacity
}
'''
# client = MongoClient('localhost', 27017)
# database = client['hwSetName']
# collection = database['hwSetName']
# Function to create a new hardware set
def createHardwareSet(db, hwSetName, initCapacity):
    # Create a new hardware set in the database
    try:
        collection = db['hwSetName']
        HardwareSet = {
            'hwName': hwSetName,
            'capacity': initCapacity,
            'availability': initCapacity
        }
        collection.insert_one(HardwareSet)
        return "Hardware Set Created Successfully"
    except Exception as e:
        return "Hardware Set Creation Error" + str(e)


# Function to query a hardware set by its name
def queryHardwareSet(db, hwSetName):
    # Query and return a hardware set from the database
    collection = db['hwSetName']
    query = collection.find_one({'hwName': hwSetName})
    return query

# Function to update the availability of a hardware set
def updateAvailability(db, hwSetName, newAvailability):
    # Update the availability of an existing hardware set
    collection = db['hwSetName']
    query = collection.find_one({'hwName': hwSetName})
    query['availability'] = newAvailability

# Function to request space from a hardware set
def requestSpace(db, hwSetName, amount):
    # Request a certain amount of hardware and update availability
    collection = db['hwSetName']
    set = queryHardwareSet(db, hwSetName)
    if set['availability'] >= amount:
        collection.update_one(
            {'hwName': hwSetName},
            {'$inc': {'availability': - amount}}
        )

# Function to get all hardware set names
def getAllHwNames(db):
    # Get and return a list of all hardware set names
    collection = db['hwSetName']
    setNames = collection.find({}, {'hwName': 1, "_id": 0})
    list = [hw['hwName'] for hw in setNames]
    return list
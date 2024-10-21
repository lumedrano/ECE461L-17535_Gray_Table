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
client = MongoClient('localhost', 27017)
database = client['hwSetName']
collection = database['hwSetName']
# Function to create a new hardware set
def createHardwareSet(client, hwSetName, initCapacity):
    # Create a new hardware set in the database
    HardwareSet = {
        'hwName': hwSetName,
        'capacity': initCapacity,
        'availability': initCapacity
    }
    collection.insert_one(HardwareSet)

# Function to query a hardware set by its name
def queryHardwareSet(client, hwSetName):
    # Query and return a hardware set from the database
    try:
        return collection.find_one({'hwName': hwSetName})
    except:
        print("There is no hwSet under that name.")

# Function to update the availability of a hardware set
def updateAvailability(client, hwSetName, newAvailability):
    # Update the availability of an existing hardware set
    query = collection.find_one({'hwName': hwSetName})
    query['availability'] = newAvailability

# Function to request space from a hardware set
def requestSpace(client, hwSetName, amount):
    # Request a certain amount of hardware and update availability
    try:
        set = queryHardwareSet(client, hwSetName)
    except:
        return
    if set['availability'] >= amount:
        collection.update_one(
            {'hwName': hwSetName},
            {'$inc': {'availability': - amount}}
        )
        # Tie requested space to the user

    else:
        print("Not enough available space.\nRequested space: " + amount + "\nAvailable space: " + set['availability'])

# Function to get all hardware set names
def getAllHwNames(client):
    # Get and return a list of all hardware set names
    setNames = collection.find({}, {'hwName': 1, "_id": 0})
    list = [hw['hwName'] for hw in setNames]
    return list

createHardwareSet(client, "hwTest1", 100)
requestSpace(client, "hwTest1", 50)
print(getAllHwNames(client))
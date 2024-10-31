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
client = MongoClient("mongodb+srv://teamAuth:QsbCrYdZbBIqDko8@ece461l.ezc85.mongodb.net/?retryWrites=true&w=majority&appName=ECE461L")
database = client['hwSetName']
collections = database['hwSetName']
# Function to create a new hardware set
#@app.route("/create_hardware_set")
def createHardwareSet(client, hwSetName, initCapacity):
    # Create a new hardware set in the database
    HardwareSet = {
        'hwName': hwSetName,
        'capacity': initCapacity,
        'availability': initCapacity
    }
    collections.insert_one(HardwareSet)

# Function to query a hardware set by its name
def queryHardwareSet(client, hwSetName):
    # Query and return a hardware set from the database
    return collections.find_one({'hwName': hwSetName})


# Function to update the availability of a hardware set
def updateAvailability(client, hwSetName, newAvailability):
    # Update the availability of an existing hardware set
    query = collections.find_one({'hwName': hwSetName})
    query['availability'] = newAvailability

# Function to request space from a hardware set
def requestSpace(client, hwSetName, amount):
    # Request a certain amount of hardware and update availability
    set = queryHardwareSet(client, hwSetName)
    if set['availability'] >= amount:
        collections.update_one(
            {'hwName': hwSetName},
            {'$inc': {'availability': - amount}}
        )

# Function to get all hardware set names
def getAllHwNames(client):
    # Get and return a list of all hardware set names
    setNames = collections.find({}, {'hwName': 1, "_id": 0})
    list = [hw['hwName'] for hw in setNames]

# test code
if __name__ == '__main__':
    createHardwareSet(client, 'test', 100)
    print(queryHardwareSet(client, 'test'))


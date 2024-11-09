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
db = client['hardware_set']
collection = db['set_collection']
app = Flask(__name__)

# Function to create a new hardware set
@app.route('/create_hardware_set', methods=['POST'])
def createHardwareSet(client, hwSetName, initCapacity):
    # Create a new hardware set in the database
    if(queryHardwareSet(client, hwSetName)):
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
def queryHardwareSet(client, hwSetName):
    # Query and return a hardware set from the database
    return collection.find_one({'hwName': hwSetName})

# Function to update the availability of a hardware set
def updateAvailability(client, hwSetName, changeInAvailability):
    # Update the availability of an existing hardware set
    collection.update_one(
        {'hwName': hwSetName},
        {'$inc': {'availability': changeInAvailability}}
    )
    return "Availability Updated Successfully"

# Function to request space from a hardware set
def requestSpace(client, hwSetName, amount):
    # Request a certain amount of hardware and update availability
    hardware_set = queryHardwareSet(client, hwSetName)
    if hardware_set and hardware_set['availability'] >= amount:
        collection.update_one(
            {'hwName': hwSetName},
            {'$inc': {'availability': -amount}}
        )
        return "Space Requested Successfully"
    return "Not Enough Availability or Hardware Set Not Found"

# Function to get all hardware set names
@app.route('/get_all_hw_sets', methods=['POST'])
def getAllHWSets(client):
    # Get and return a list of all hardware sets
    HWsets = collection.find({}, {'hwName': 1, 'capacity': 1, 'availability': 1, '_id': 0})
    setsList = list(HWsets)
    return setsList

# test code
if __name__ == '__main__':
    # Clear collection at start
    collection.delete_many({})
    print(createHardwareSet(client, 'test', 100))
    print(createHardwareSet(client, 'dog', 200))
    print(createHardwareSet(client, 'test', 200))
    print(queryHardwareSet(client, 'test'))
    print(requestSpace(client, 'test', 50))
    print(updateAvailability(client, 'test', -20))
    print(queryHardwareSet(client, 'test'))
    setsList = getAllHWSets(client)
    print("Listing all HWSets: ")
    for i in setsList:
        print(i)


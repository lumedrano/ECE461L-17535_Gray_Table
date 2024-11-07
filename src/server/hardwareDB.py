# Import necessary libraries and modules
from dataclasses import dataclass
from flask import Flask, request, jsonify
from pymongo import MongoClient

'''
Structure of Hardware Set entry:
HardwareSet = {
    'hwName': hwSetName,
    'capacity': initCapacity,
    'availability': initCapacity
}
'''
# client = MongoClient("mongodb+srv://teamAuth:QsbCrYdZbBIqDko8@ece461l.ezc85.mongodb.net/?retryWrites=true&w=majority&appName=ECE461L")
# Function to create a new hardware set
#@app.route("/create_hardware_set")
def createHardwareSet(db, hwSetName, initCapacity):
    # Create a new hardware set in the database
    HardwareSet = {
        'hwName': hwSetName,
        'capacity': initCapacity,
        'availability': initCapacity
    }
    db['hardware_sets'].insert_one(HardwareSet)
    return "Hardware Set Created Successfully"

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
    pass

# test code
# if __name__ == '__main__':
#     createHardwareSet(client, 'test', 100)
#     print(queryHardwareSet(client, 'test'))


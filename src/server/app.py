
# Import necessary libraries and modules
from bson.objectid import ObjectId
from flask import Flask, request, jsonify
from pymongo import MongoClient

# Import custom modules for database interactions
import usersDB
import projectsDB
import hardwareDB
from database import get_database

# Define the MongoDB connection string
# MONGODB_SERVER = "your_mongodb_connection_string_here"

#TODO: would it be better to create and close connections on here or on usersDB/projectsDB/hardwareDB python files?
#TODO; look into if I should use if statements on here with status codes 200, 201, 404, etc.
#TODO: Query: i have a database.py file [insert file] that connects to MongoDB, I use it in usersDB and plan on using it within two other files, should I instead use it in my main app.py file to connect/close for each function call?

# Initialize a new Flask web application
app = Flask(__name__)

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    # Extract data from request
    data = request.json
    user = data.get('username')
    userId = data.get('userId')
    password = data.get('password')

    # Attempt to log in the user using the usersDB module
    result = usersDB.login(user, userId, password)

    # Return a JSON response
    return jsonify({'message: ': result})

# Route for the main page (Work in progress)
@app.route('/main')
def mainPage():
    # Extract data from request

    # Connect to MongoDB

    # Fetch user projects using the usersDB module

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for joining a project
@app.route('/join_project', methods=['POST'])
def join_project():
    # Extract data from request
    data = request.json
    userId = data.get('userId')
    projectId = data.get('projectId')

    # Attempt to join the project using the usersDB module
    result = usersDB.joinProject(userId, projectId)
    # Return a JSON response
    return jsonify({'message': result})

# Route for adding a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    # Extract data from request
    data = request.json
    user = data.get('username')
    userId= data.get('userId')
    password = data.get('password')

    # Attempt to add the user using the usersDB module
    result = usersDB.addUser(user, userId, password)

    # Return a JSON response
    return jsonify({'message': result})

# Route for getting the list of user projects
@app.route('/get_user_projects_list', methods=['POST'])
def get_user_projects_list():
    # Extract data from request
    data = request.json
    userId = data.get('userId')

    # Fetch the user's projects using the usersDB module
    result = usersDB.getUserProjectsList(userId)

    # Return a JSON response
    return jsonify({'message': result})

# Route for creating a new project
@app.route('/create_project', methods=['POST'])
def create_project():
    # Extract data from request

    # Connect to MongoDB

    # Attempt to create the project using the projectsDB module

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for getting project information
@app.route('/get_project_info', methods=['POST'])
def get_project_info():
    # Extract data from request

    # Connect to MongoDB

    # Fetch project information using the projectsDB module

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for getting all hardware names
@app.route('/get_all_hw_names', methods=['POST'])
def get_all_hw_names():
    # Connect to MongoDB

    # Fetch all hardware names using the hardwareDB module

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for getting hardware information
@app.route('/get_hw_info', methods=['POST'])
def get_hw_info():
    # Extract data from request

    # Connect to MongoDB

    # Fetch hardware set information using the hardwareDB module

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for checking out hardware
@app.route('/check_out', methods=['POST'])
def check_out():
    # Extract data from request

    # Connect to MongoDB

    # Attempt to check out the hardware using the projectsDB module

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for checking in hardware
@app.route('/check_in', methods=['POST'])
def check_in():
    # Extract data from request

    # Connect to MongoDB

    # Attempt to check in the hardware using the projectsDB module

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for creating a new hardware set
@app.route('/create_hardware_set', methods=['POST'])
def create_hardware_set():
    # Extract data from request

    # Connect to MongoDB

    # Attempt to create the hardware set using the hardwareDB module

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Route for checking the inventory of projects
@app.route('/api/inventory', methods=['GET'])
def check_inventory():
    # Connect to MongoDB

    # Fetch all projects from the HardwareCheckout.Projects collection

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({})

# Main entry point for the application
if __name__ == '__main__':
    app.run()

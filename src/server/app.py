
# Import necessary libraries and modules
from bson.objectid import ObjectId
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# Import custom modules for database interactions
import usersDB
import projectsDB
import hardwareDB

# Define the MongoDB connection string
# MONGODB_SERVER = "your_mongodb_connection_string_here"

#TODO; look into if I should use if statements on here with status codes 200, 201, 404, etc.

# Initialize a new Flask web application
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


#load in environmental variables
load_dotenv()

@app.before_request
def before_request():
    g.client = MongoClient(os.getenv('MONGODB_CONNECTION_STRING'), server_api=ServerApi('1'), tls=True, tlsAllowInvalidCertificates=True)
    g.db = g.client['ece461l_final_project']

@app.teardown_request
def teardown_request(exc=None):
    client = g.pop('client', None)
    if client:
        client.close()


# Route for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    userId = data.get('userId')
    password = data.get('password')

    if not all([username, userId, password]):
        return jsonify({'message': 'Username, userId, and password are required.'}), 400

    result = usersDB.login(g.db, username, userId, password)

    if result == "Login Successful!":
        return jsonify({'message': result, 'userId': userId}), 200
    elif result == "Invalid password.":
        return jsonify({'message': result}), 401
    else:
        return jsonify({'message': result}), 400

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
    data = request.json
    userId = data.get('userId')
    projectId = data.get('projectId')

    if not all([userId, projectId]):
        return jsonify({'message': 'userId and projectId are required.'}), 400

    result = usersDB.joinProject(g.db, userId, projectId)

    if result == "Successfully added to project!":
        return jsonify({'message': result}), 200
    elif result == "User not found":
        return jsonify({'message': result}), 404
    else:
        return jsonify({'message': result}), 400

# Route for adding a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    username = data.get('username')
    userId = data.get('userId')
    password = data.get('password')

    if not all([username, userId, password]):
        return jsonify({'message': 'Username, userId, and password are required.'}), 400

    result = usersDB.addUser(g.db, username, userId, password)

    if result == "User added successfully.":
        return jsonify({'message': result, 'userId': userId}), 201
    else:
        return jsonify({'message': result}), 400

# Route for getting the list of user projects
@app.route('/get_user_projects_list', methods=['POST'])
def get_user_projects_list():
    data = request.json
    userId = data.get('userId')

    if not userId:
        return jsonify({'message': 'userId is required.'}), 400

    result = usersDB.getUserProjectsList(g.db, userId)

    if isinstance(result, list):
        return jsonify({'projects': result}), 200
    else:
        return jsonify({'message': result}), 404

# Route for creating a new project
@app.route('/create_project', methods=['POST'])
def create_project():
    # Extract data from request
    data = request.json
    projectName = data['projectName']
    projectId = data['projectId']
    description = data['description']

    result = projectsDB.createProject(g.db, projectName, projectId, description)

    if result == "project created successfully":
        return jsonify({'message': result, 'projectId': projectId}), 201
    else:
        return jsonify({'message': result}), 400


# Route for getting project information
@app.route('/get_project_info', methods=['POST'])
def get_project_info():
    # Extract data from request
    data = request.json
    projectId = data['projectId']


    # Connect to MongoDB

    # Fetch project information using the projectsDB module
    #TODO: fetch using user's information
    result = projectsDB.queryProject(g.db, projectId)
    # Close the MongoDB connection

    # Return a JSON response

    if result == None:
        return jsonify({'message: Project Query Error'})
    else:
        return jsonify({'project:', result})

# Route for getting all hardware names
@app.route('/get_all_hw_names', methods=['POST'])
def get_all_hw_names():
    # Connect to MongoDB

    # Fetch all hardware names using the hardwareDB module
    result = hardwareDB.getAllHwNames(g.db)

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({'message': result}), 200

# Route for getting hardware information
@app.route('/get_hw_info', methods=['POST'])
def get_hw_info():
    # Extract data from request
    data = request.json
    hwSetName = data['hwSetName']
    # Connect to MongoDB

    # Fetch hardware set information using the hardwareDB module
    result = hardwareDB.queryHardwareSet(g.db, hwSetName)

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({'message': result}), 200

# Route for checking out hardware
@app.route('/check_out', methods=['POST'])
def check_out():
    # Extract data from request
    data = request.json
    projectId = data['projectId']
    hwSetName = data['hwSetName']
    amount = data['qty']
    userId = data['userId']
    # Connect to MongoDB

    # Attempt to check out the hardware using the projectsDB module
    result = projectsDB.checkOutHW(g.db, projectId, hwSetName, amount, userId)

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({'message': result}), 200

# Route for checking in hardware
@app.route('/check_in', methods=['POST'])
def check_in():
    # Extract data from request
    data = request.json
    projectId = data['projectId']
    hwSetName = data['hwSetName']
    amount = data['qty']
    userId = data['userId']

    # Connect to MongoDB

    # Attempt to check in the hardware using the projectsDB module
    result = projectsDB.checkInHW(g.db, projectId, hwSetName, amount, userId)
    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({'message': result}), 200

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
    app.run(debug=True, ssl_context=None)  # Disable SSL for development


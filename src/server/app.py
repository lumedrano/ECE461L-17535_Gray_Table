
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


# Initialize a new Flask web application
app = Flask(__name__)
#TODO: use the following line instead of the above when deploying code to heroku
# app = Flask(__name__, static_folder="./build", static_url_path='/')

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

    #mapping all responses back to front end
    if result == "Successfully joined project!":
        return jsonify({'message': result}), 200
    elif result == "Project not found":
        return jsonify({'message': result}), 404
    elif result == "User is already a member of this project" or result == "No changes needed - user already in project":
        return jsonify({'message': result}), 409  # conflict status code
    elif result.startswith("An error occurred"):
        return jsonify({'message': result}), 500  # server-side error
    else:
        return jsonify({'message': result}), 400 

# Route for removing a user from a project using projectId
@app.route('/leave_project', methods=['POST'])
def leave_project():
    data = request.json
    userId = data.get('userId')
    projectId = data.get('projectId')

    if not all([userId, projectId]):
        return jsonify({'message': 'userId and projectId are required.'}), 400

    result = usersDB.leaveProject(g.db, userId, projectId)

    # Mapping responses back to the frontend
    if result == "Successfully left the project":
        return jsonify({'message': result}), 200
    elif result == "Project not found":
        return jsonify({'message': result}), 404
    elif result == "User is not a member of this project":
        return jsonify({'message': result}), 409  # conflict status code
    elif result.startswith("An error occurred"):
        return jsonify({'message': result}), 500  # server-side error
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
#TODO: maybe upon successful login of user, call this function to populate the projects page with user's project information.
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







#Project handlers Below

# Route for creating a new project@app.route('/create_project', methods=['POST'])
@app.route('/create_project', methods=['POST'])
def create_project():
    try:
        data = request.json
        
        # validate required fields
        required_fields = ['projectName', 'projectId', 'description', 'userID']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'Missing required field: {field}'}), 400
                
        projectName = data['projectName']
        projectId = data['projectId']
        description = data['description']
        userID = data['userID']
        
        if not all([projectName, projectId, description, userID]):
            return jsonify({'message': 'Fill out all fields.'}), 400

        result = projectsDB.createProject(g.db, projectName, projectId, description, userID)

        if result == "Project created successfully":
            return jsonify({
                'message': result, 
                'projectId': projectId,
                'projectName': projectName
            }), 201
        else:
            return jsonify({'message': result}), 400
            
    except Exception as e:
        return jsonify({'message': f'Server error: {str(e)}'}), 500



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
        return jsonify({'message: Project Query Error'}), 404
    else:
        return jsonify({'project info:', result}), 200
    
# Route for checking out hardware
@app.route('/check_out', methods=['POST'])
def check_out():
    # Extract data from request
    data = request.json
    projectId = data['projectId']
    hwSetName = data['hwSetName']
    qty = data['qty']
    userId = data['userId']
    # Connect to MongoDB

    # Attempt to check out the hardware using the projectsDB module
    result = projectsDB.checkOutHW(g.db, projectId, hwSetName, qty, userId)
    if(result == "Successfully checked out."):
        # Return success response if successful
        return jsonify({'message': result}), 200
    # Close the MongoDB connection
    
    # Return failure message if result is anything else
    return jsonify({'message': result,}), 400

# Route for checking in hardware
@app.route('/check_in', methods=['POST'])
def check_in():
    # Extract data from request
    data = request.json
    projectId = data['projectId']
    hwSetName = data['hwSetName']
    qty = data['qty']
    userId = data['userId']

    # Connect to MongoDB

    # Attempt to check in the hardware using the projectsDB module
    result = projectsDB.checkInHW(g.db, projectId, hwSetName, qty, userId)
    if(result == "Successfully checked in."):
        # Return success response if successful
        return jsonify({'message': result}), 200
    # Close the MongoDB connection
    
    # Return failure message if result is anything else
    return jsonify({'message': result,}), 400





#HardwareSet handlers Below


# Route for getting all hardware sets in a list
@app.route('/get_all_hw_sets', methods=['POST'])
def get_all_hw_sets():
    # Connect to MongoDB

    # Fetch all hardware sets using the hardwareDB module
    result = hardwareDB.getAllHWSets(g.db)
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


# Route for creating a new hardware set
@app.route('/create_hardware_set', methods=['POST'])
def create_hardware_set():
    try:
    # Extract data from request
        data = request.json
        print("Received data: ", data)

        hwSetName = data.get('hwSetName')
        initCapacity = data.get('initCapacity')
    # Connect to MongoDB

    # Attempt to create the hardware set using the hardwareDB module
        if initCapacity is not None:
            try:
                initCapacity = int(initCapacity)
            except ValueError:
                return jsonify({'message': 'initCapacity must be an integer.'}), 400

        print(f"hwSetName: {hwSetName}, initCapacity: {initCapacity}")

        if not hwSetName or initCapacity is None:
            return jsonify({'message': 'hwSetName and initCapacity are required.'}), 400

        result = hardwareDB.createHardwareSet(g.db, hwSetName, initCapacity)
    # Close the MongoDB connection

    # Return a JSON response
        if result == "Hardware Set Created Successfully":
            return jsonify({'message': result}), 201
        else:
            return jsonify({'message': result}), 400

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({'message': f"Server error: {str(e)}"}), 500

# Route for checking the inventory of projects
@app.route('/api/inventory', methods=['GET'])
def check_inventory():
    data = request.json
    # Connect to MongoDB

    # Fetch all projects from the HardwareCheckout.Projects collection
    collection = g.db['HardwareCheckout']
    projects = collection['Projects']

    # Close the MongoDB connection

    # Return a JSON response
    return jsonify({projects}), 200

#index.html is the page we want to load as soon as the flask app starts. from the build folder after running npm run build
# @app.route('/')
# def index():
#     return app.send_static_file('index.html')

# Main entry point for the application
if __name__ == '__main__':
    app.run(debug=True, ssl_context=None)  # Disable SSL for development


#Kimberly & Luigi

#using MongoDB through python
from database import get_database
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import cipher


#for reference
'''
Structure of User entry:
User = {
    'username': username,
    'userId': userId,
    'password': password,
    'projects': [project1_ID, project2_ID, ...]
}
'''

#TODO: may need to edit MONGODB Client to CLOSE connection after each call to function


# Global variables for client and collection
client = None
collection = None

def get_collection():
    global client, collection
    if collection is None:
        client = get_database()
        if client is not None:
            db = client['ece461l_final_project']
            collection = db['usersDB']
        else:
            raise Exception("Failed to connect to the database")
    return collection

# Function to add a new user
def addUser(username, userId, password):
    if not username or not userId or not password:
        return "Username, userId, and password are required."
    try:
        collection = get_collection()
        # Add a new user to the database
        if collection.find_one({'username': username, 'userId': userId}):
            return "User already exists."
        encryptedpassword = cipher.encrypt(password, 3, 1)
        new_user = {
            'username': username,
            'userId': userId,
            'password': encryptedpassword,
            'projects': []
        }
        
        result = collection.insert_one(new_user)
        if result.acknowledged:
            return "User was added successfully."
        else:
            return "Failed to add user."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Helper function to query a user by username and userId
def __queryUser(username, userId):
    try:
        collection = get_collection()
        # Query and return a user from the database
        return collection.find_one({'username': username, 'userId': userId})
    except Exception as e:
        print(f"An error occurred while querying user: {str(e)}")
        return None

# Function to log in a user
def login(username, userId, password):
    if not username or not userId or not password:
        return "Username, userId, and password are required."
    try:
        #find person using query function from above
        user = __queryUser(username, userId)
        #check if user is found, if so then use decrypt function on password by passing password in
        if user:
            encrypted_pw = user['password']
            decrypted_pw = cipher.decrypt(encrypted_pw, 3, 1)
            
            #if match then return something that they are logged in
            if decrypted_pw == password:
                return "Login Successful!"
            #if not, return error message saying invalid 
            return "Invalid password."
        #if user was not found by username/id then return user not found
        return "User not found."
    except Exception as e:
        return f"An error occurred during login: {str(e)}"

# Function to add a user to a project
def joinProject(userId, projectId):
    if not userId or not projectId:
        return "userId and projectId are required."
    try:
        collection = get_collection()
        # Add a user to a specified project
        if not collection.find_one({'userId': userId}):
            return "User not found"
        
        result = collection.update_one(
            {'userId': userId},
            {'$addToSet': {'projects': projectId}}
        )

        if result.modified_count > 0:
            return "Successfully added to project!"
        else:
            return "Already added to project."
    except Exception as e:
        return f"An error occurred while joining project: {str(e)}"

# Function to get the list of projects for a user
def getUserProjectsList(userId):
    if not userId:
        return "userId is required."
    try:
        collection = get_collection()
        # Get and return the list of projects a user is part of

        #find user in db
        user = collection.find_one({'userId': userId})
        
        # if found use .get to obtain projects
        if user:
            return user.get('projects', [])
        else:
            return "User not found"
    except Exception as e:
        return f"An error occurred while getting user projects: {str(e)}"
    
# test statements for the project functions
# def test_joinProject():
#     # attempt to add a user to a project
#     print("Testing joinProject...")
#     result = joinProject("1001", "project001")
#     print(f"Join Project Result: {result}")
    
#     # attempt to add the same user to the same project again
#     result = joinProject("1001", "project001")
#     print(f"Join Project Again (should indicate already added): {result}")

# def test_getUserProjectsList():
#     # attempt to get the list of projects for the user
#     print("Testing getUserProjectsList...")
#     projects = getUserProjectsList("1001")
#     print(f"User Projects List: {projects}")

# if __name__ == "__main__":
#     print("Testing addUser and login functions...")
#     print(addUser("Luigi", "1001", "test123"))
#     print(login("Luigi", "1001", "test123"))
#     print(login("Luigi", "1001", "test122"))

#     print("\nTesting project functions...")
#     test_joinProject()
#     test_getUserProjectsList()

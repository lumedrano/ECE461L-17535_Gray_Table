from database import get_database
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

def addUser(username, userId, password):
    try:
        collection = get_collection()
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

def __queryUser(username, userId):
    try:
        collection = get_collection()
        return collection.find_one({'username': username, 'userId': userId})
    except Exception as e:
        print(f"An error occurred while querying user: {str(e)}")
        return None

def login(username, userId, password):
    try:
        user = __queryUser(username, userId)
        if user:
            encrypted_pw = user['password']
            decrypted_pw = cipher.decrypt(encrypted_pw, 3, 1)
            if decrypted_pw == password:
                return "Login Successful!"
            return "Invalid password."
        return "User not found."
    except Exception as e:
        return f"An error occurred during login: {str(e)}"

def joinProject(userId, projectId):
    try:
        collection = get_collection()
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

def getUserProjectsList(userId):
    try:
        collection = get_collection()
        user = collection.find_one({'userId': userId})
        if user:
            return user.get('projects', [])
        else:
            return "User not found"
    except Exception as e:
        return f"An error occurred while getting user projects: {str(e)}"
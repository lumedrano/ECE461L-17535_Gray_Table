#Kimberly & Luigi
import cipher

'''
Structure of User entry:
User = {
    'username': username,
    'userId': userId,
    'password': password,
    'projects': [project1_ID, project2_ID, ...]
}
'''

# Function to add a new user
def addUser(db, username, userId, password):
    collection = db['usersDB']
    if not username or not userId or not password:
        return "Username, userId, and password are required."
    try:
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
            return "User added successfully."
        else:
            return "Failed to add user."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Helper function to query a user by username and userId
def __queryUser(db, username, userId):
    collection = db['usersDB']
    try:
        # Query and return a user from the database
        return collection.find_one({'username': username, 'userId': userId})
    except Exception as e:
        print(f"An error occurred while querying user: {str(e)}")
        return None

# Function to log in a user
def login(db, username, userId, password):
    collection = db['usersDB']
    if not username or not userId or not password:
        return "Username, userId, and password are required."
    try:
        # Find person using query function from above
        user = __queryUser(db, username, userId)
        # Check if user is found, if so then use decrypt function on password by passing password in
        if user:
            encrypted_pw = user['password']
            decrypted_pw = cipher.decrypt(encrypted_pw, 3, 1)
            
            # If match, return success message
            if decrypted_pw == password:
                return "Login Successful!"
            # If not, return error message
            return "Invalid password."
        # If user was not found by username/id, return user not found
        return "User not found."
    except Exception as e:
        return f"An error occurred during login: {str(e)}"

# Function to add a user to a project
def joinProject(db, userId, projectId):
    users_collection = db['usersDB']
    projects_collection = db['projectsDB']
    
    #convert to strings for comparing
    #TODO: when further implementing, check if we need to keep IDs in integer or if they can be mix type
    userId = str(userId)
    projectId = str(projectId)
    
    if not userId or not projectId:
        return "userId and projectId are required."
    
    try:
        # First verify user exists with string userId
        user = users_collection.find_one({'userId': userId})
        if not user:
            print(f"User not found with userId: {userId}")
            return "User not found"
            
        # Check if project exists
        project = projects_collection.find_one({'projectId': projectId})
        if not project:
            return "Project not found"
            
        # Check if user is already in project's users list
        if 'users' in project and userId in project['users']:
            return "User is already a member of this project"
        
        # Update project's users list
        project_result = projects_collection.update_one(
            {'projectId': projectId},
            {'$push': {'users': userId}}
        )
        
        # Update user's projects list
        user_result = users_collection.update_one(
            {'userId': userId},
            {'$push': {'projects': projectId}}
        )
        
        if project_result.modified_count > 0 and user_result.modified_count > 0:
            return "Successfully joined project!"
        else:
            # Rollback project update if user update failed
            if project_result.modified_count > 0 and user_result.modified_count == 0:
                projects_collection.update_one(
                    {'projectId': projectId},
                    {'$pull': {'users': userId}}
                )
            return "Failed to update user record"
            
    except Exception as e:
        print(f"Exception details: {str(e)}")
        return f"An error occurred while joining project: {str(e)}"

# Function to get the list of projects for a user
def getUserProjectsList(db, userId):
    collection = db['usersDB']
    if not userId:
        return "userId is required."
    try:
        # get and return the list of projects a user is part of
        user = collection.find_one({'userId': userId})
        
        # if found, use .get to obtain projects
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




# <--------------- FLASK  ------------------>
# IMPORT FLASK TO CREATE APP
# <--------------------------------------------> 
# this holds all the important info.  
# jsonify let's us send JSON HTTP responses (like res.json)
from flask import Flask, jsonify




# <------------- BLUEPRINTS  ---------------->
# GLOBAL SCOPE IMPORT FOR MODELS / CONTROLLERS
# <--------------------------------------------> 
# importing blueprints from resources. 
# TICKETS
# from resources.tickets import tickets
# # PROJECTS
# from resources.projects import projects
# # TEAMS
# from resources.teams import teams
# # USERS
from resources.users import users 




# <--------------- MODELS  ------------------>
# IMPORT MODELS FILE TO ACCESS IT HERE 
# <--------------------------------------------> 
# This will start the models file when our app starts. 
import models 




# <--------------- CORS  ------------------>
# CROSS ORIGIN RESOURCE SHARING 
# <--------------------------------------------> 
# allow CORS for all domains and routes.  
from flask_cors import CORS 




# <----------- LOGIN MANAGER  ---------------->
# IMPORT LOGIN MANAGER HERE 
# <--------------------------------------------> 
# Tool for coordinating sessions and login in the app. 
from flask_login import LoginManager 




# <---------- DEBUGGING SETUP -------------->
# SETUP FOR ERROR HANDLING 
# <--------------------------------------------> 
# Provides helpful error message on port 8000 for debugging. 
DEBUG=True
PORT=8000



# <--------------- FLASK APP  ------------------>
# USE FLASK TO CREATE APP 
# <--------------------------------------------> 
# Instantiating the Flask class to create an app. 
app = Flask(__name__)




# <------ LOGIN MANAGER SETUP  -------->
# CONFIGURE LOGIN MANAGER HERE  
# <--------------------------------------------> 
# Configuring LoginManager, with secret/key, instantiation, and connection. 
# SECRET/KEY SETUP 
app.secret_key = "This is a huge secret."
# INSTANTIATE 
login_manager = LoginManager()
# CONNECTION 
login_manager.init_app(app)


# USER LOADER  -------->
@login_manager.user_loader # this allows access to User Object
def load_user(user_id):
  try:
    print("loading the following user")
    user = models.User.get_by_id(user_id)
    return models.User.get(user_id)
  except models.DoesNotExist:
    return None

@login_manager.unauthorized_handler
def unauthorized():
  return jsonify(
    data={
      'error': 'User not logged in'
    }, 
    message="You must be logged in to access that resource", 
    status=401
  ), 401



# <----------- CORS SETUP -------------->
# SETUP FOR CORS 
# <--------------------------------------------> 
# Setup for each model 
CORS(users, origins=['http://localhost:3000'],
  supports_credentials=True)

# CORS(teams, origins=['http://localhost:3000'],
#   supports_credentials=True)

# CORS(projects, origins=['http://localhost:3000'],
#   supports_credentials=True)

# CORS(tickets, origins=['http://localhost:3000'],
#   supports_credentials=True)




# <----------- BLUEPRINT SETUP  -------------->
# SETUP FOR BLUEPRINTS 
# <--------------------------------------------> 
# Controller of the app
app.register_blueprint(users, url_prefix='/api/v1/users')

# app.register_blueprint(teams, url_prefix='/api/v1/teams')

# app.register_blueprint(projects, url_prefix='/api/v1/projects')

# app.register_blueprint(tickets, url_prefix='/api/v1/tickets')



# <----------- TEST ROUTES  -------------->
# TESTING 
# <--------------------------------------------> 
# Testing successful connection of the app 
@app.route('/')
def hello():
  return 'MARA is now working!'



# <----------- LISTENER  -------------->
# LISTENER FOR THE APP  
# <--------------------------------------------> 
# This runs the application 
if __name__ == '__main__':
  models.initialize() #when we start the app setup the database. 
  app.run(debug=DEBUG, port=PORT)

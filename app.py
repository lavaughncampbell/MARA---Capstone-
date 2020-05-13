


# <--------------- FLASK  ------------------>
# IMPORT FLASK TO CREATE APP
# <--------------------------------------------> 
# this holds all the important info.  
# jsonify let's us send JSON HTTP responses (like res.json)
from flask import Flask, jsonify, url_for, redirect, session




# TESTING TESTING TESTING OAUTH 
from authlib.integrations.flask_client import OAuth













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
# TESTING TESTING TESTING OAUTH 
# oauth config 
oauth = OAuth(app)
google = oauth.register(
  name='google',
    client_id='132211331164-g91rvmn983kcrd8amu1c4g84sl3riac8.apps.googleusercontent.com',
    client_secret='Cr9jvd6hgSnjmAYhPq2HN-lb',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    # userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)


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
  email = dict(session).get('email', None)
  return f'Hello, {email}!'

# TESTING TESTING TESTING OAUTH 
@app.route('/login')
def login():
  google = oauth.create_client('google')
  redirect_uri = url_for('authorize', _external=True)
  return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
  google = oauth.create_client('google')
  token = google.authorize_access_token()
  resp = google.get('userinfo')
  user_info = resp.json()
  # do something with the token and profile
  session['email'] = user_info['email']
  return redirect('/')



# <----------- LISTENER  -------------->
# LISTENER FOR THE APP  
# <--------------------------------------------> 
# This runs the application 
if __name__ == '__main__':
  models.initialize() #when we start the app setup the database. 
  app.run(debug=DEBUG, port=PORT)




# <--------------- FLASK  ------------------>
# IMPORT FLASK TO CREATE APP
# <--------------------------------------------> 
# this holds all the important info.  
# jsonify let's us send JSON HTTP responses (like res.json)
# updated flask import with url_for, redirect, session for google. 
# also installed requests for google 
from flask import Flask, jsonify, url_for, redirect, session


# <--------------- AUTHLIB  ------------------>
# IMPORT AUTHLIB FOR OAUTH
# <--------------------------------------------> 
# installed Authlib for building OAuth and OpenID connect
from authlib.integrations.flask_client import OAuth




# <------------- BLUEPRINTS  ---------------->
# GLOBAL SCOPE IMPORT FOR MODELS / CONTROLLERS
# <--------------------------------------------> 
# importing blueprints from resources. 
# TICKETS
# from resources.tickets import tickets
# # PROJECTS
# from resources.projects import projects
# # MEMBERS
from resources.members import members
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




# <--------------- GOOGLE LOGIN  ------------------>
# OAUTH CONFIGURATION FOR GOOGLE 
# <--------------------------------------------> 
# Configuring the google login 
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

# use this blueprint (component/piece/section/controller of the app) 
app.register_blueprint(members, url_prefix='/api/v1/members')
# similar to app.use('/api/v1/members', memberController)
# app.register_blueprint(projects, url_prefix='/api/v1/projects')

# app.register_blueprint(tickets, url_prefix='/api/v1/tickets')




# <----------- GOOGLE ROUTES -------------->
# GOOGLE OAUTH ROUTES 
# <--------------------------------------------> 
# This goes to google to authenticate the user.  

# <---- Home -----> 
@app.route('/')
def hello():
  email = dict(session).get('email', None)
  return f'Hello, {email}!'

# <---- Login -----> 
@app.route('/login')
def login():
  google = oauth.create_client('google')
  redirect_uri = url_for('authorize', _external=True)
  return google.authorize_redirect(redirect_uri)

# <---- Authorize -----> 
@app.route('/authorize')
def authorize():
  google = oauth.create_client('google')
  token = google.authorize_access_token()
  resp = google.get('userinfo')
  user_info = resp.json()
  # do something with the token and profile
  session['email'] = user_info['email']
  return redirect('/')

# <---- Logout -----> 
@app.route('/logout')
def logout():
  for key in list(session.keys()):
    session.pop(key)
  return redirect('/') 


# <----------- LISTENER  -------------->
# LISTENER FOR THE APP  
# <--------------------------------------------> 
# This runs the application 
if __name__ == '__main__':
  models.initialize() #when we start the app setup the database. 
  app.run(debug=DEBUG, port=PORT)

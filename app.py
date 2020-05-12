# this is like a user controller
# or auth controller

import models # get all the models. specifically user model

from flask import Blueprint, request, jsonify # Blueprint is how we make our controllers

from flask_bcrypt import generate_password_hash, check_password_hash # to generate password hash
                        # this is a function that returns a scrambled pw

from playhouse.shortcuts import model_to_dict
# we can jsonify our models with this import
from flask_login import login_user, current_user, logout_user # login_user will be used to do the session stuff we did manually in express.




# make this a blueprint
users = Blueprint('users', 'users')

@users.route('/', methods=['GET'])
def test_user_resource():
  return "user resource works"





# <-------------------------------------->
# REGISTRATION ROUTE //


# registration will be POST because were sending
# req.body there is going to be JSON
@users.route('/register', methods=['POST'])
def register():
  # this step is similar to making sure we can log
  # req.body in express.
  # note: we had to send JSON from postman(choose raw, select
  # JSON from the drop down menu, and type a perfect JSON object with
  # double qoutes around the keys
  payload = request.get_json()
  # print(payload)

  # since emails are case insensitive in the world
  # this makes the email lowercase
  payload['email'] = payload['email'].lower()
  # might as well do the same with username
  payload['username'] = payload['username'].lower()
  print(payload) # that's better

# see if the user exists
  try:

    models.User.get(models.User.email == payload['email'])
  # this will throw an eror ()
  # shortcut method for select().where().execute_query is .get()
# if so -- we don't want to create the user
  # response: "user with that email already exist"
    return jsonify(
      data={},
      message=f"A user with that email {payload['email']} already exists",
      status=401
    ), 401

# if the user does not exist
  except models.DoesNotExist: # except is like catch in JS
  # create them!

    pw_hash = generate_password_hash(payload['password'])

    created_user = models.User.create(
      username=payload['username'],
      email=payload['email'],
      password=pw_hash,
      name=payload['name'],
      bootcamp=payload['bootcamp'],
      position=payload['position']
    )

    print(created_user)

    # this is where we will actually use flask-login
    # this "logs" in user and starts a session
    login_user(created_user)

    # respond with new object and success message

    # jsonify our models
    created_user_dict = model_to_dict(created_user)
    # we can't jsonify the password (generate_password_has gives us
    print(type(created_user_dict['password']))
    # this will get rid of the error
    created_user_dict.pop('password')

    return jsonify(
      data=created_user_dict,
      message=f"Successfully registered user {created_user_dict['email']}",
      status=201
    ), 201





# <-------------------------------------->
# LOGIN ROUTE //

# there is no route to show a register / login forms
# we dont need to the react will have the forms handled for us
@users.route('/login', methods=['POST'])
def login():
  payload = request.get_json()
  payload['email'] = payload['email'].lower()
  payload['username'] = payload['username'].lower()

  try:
    user = models.User.get(models.User.email == payload['email'])

    user_dict = model_to_dict(user)
    # check pw using bcrypt
    # check password has 2 args
    # the encrypted pw you are checking against
    # the pw attempt you are verifying
    password_is_good = check_password_hash(user_dict['password'], payload['password'])

    if(password_is_good):
      # LOG THE USER IN!!!! using Flask-Login!
      login_user(user) # in express we did this manually by stuff in session


      # respond -- all good -- remove the pw first
      user_dict.pop('password')

      return jsonify(
        data=user_dict,
        message=f"Successfully logged in {user_dict['email']}",
        status=200
      ), 200

    # else if pw is bad
    else:
      print('pw is no good')
      # respond -- bad username or password
      return jsonify(
        date={},
        message="Email or password is incorrect",
        status=401
      ), 401




  except models.DoesNotExist:
  # else if they don't exist
    print('username is no good')
    # respond -- bad username or password
    return jsonify(
      date={},
      message="Email or password is incorrect",
      status=401
    ), 401




# TEMPORARY HELPER ROUTE GET /api/v1/users/all


# temporary helper route, it will list the users, so we an pick an id
# and use that id to manually create a post connected to a user
# we might delete this later, it's ujust a tool for building / testing API
@users.route('/all', methods=['GET'])
def user_index():
  users = models.User.select()
  user_dicts = [model_to_dict(user) for user in users ]

  # remove the passwords
  for user_dict in user_dicts:
    user_dict.pop('password')

  return jsonify(user_dicts), 200

  # another route for just demonstration
  # it will j=show us who is logged in
  # once you logged in user you can him with current_user
  # we can access via current_user
  # this is what setting up user_load in our app.py allowed us to do

@users.route('/logged_in_user', methods=['GET'])
def get_logged_in_user():

  # you can tell if a user is logged in using
  # current_user.is_authenticated
  if not current_user.is_authenticated:
    return jsonify(
      data={},
      message="No user is currently logged in",
      status=401,
    ), 401

  else:
  # we can access current_user bc we called login_user and set up user_loader
    user_dict = model_to_dict(current_user)
    user_dict.pop('password')
  # OBSERVE -- YOU now have access to the currently logged in user
  # anywhere you want using current_user
  return jsonify(
    data=user_dict,
    message=f"Currently logged in as {user_dict['email']}.",
    status=200
  ), 200









# <-------------------------------------->
  # LOGOUT ROUTE //

  # we need a logout route
  # you have noticed that the session persists (i.e. user is still logged in )
  # after restarting the server
  # weird.
@users.route('/logout', methods=['GET'])
def logout():
  logout_user()
  return jsonify(
    data={},
    message="Successfully logged out.",
    status=200
  ), 200


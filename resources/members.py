# this file is similar to memberCon
import models


# blueprint is a way to create a self-contained grouping 
from flask import Blueprint, request
# request is --- data from clients is sent to the global request object 
# we can use this objet to get the json or form data or whatever 
# POST OR PUT requests have bodies


# creating our blueprint
# first arg is blueprint name 
# second arg is its import name  
# similar to createing a router in express 
members = Blueprint('members', 'members')

# ----------># ----------># ---------->
# INDEX 

# GET /api/v1/members 
@members.route('/', methods=['GET'])
def members_index():
  return "members resource working"

  # WE DONT WANT TO REALLY GET INTO A INDEX ROUTE BEFORE CREATE ROUTE 



# ----------># ----------># ---------->
# CREATE 

# POST /api/v1/members 
# SPECIFY THE HTTP METHOD 
# this is like app.posts 
@members.route('/', methods=['POST'])
def create_member():
  # request has a helpful method that will take data in a request 
  # and give it to us as JSON 
  # store this info in a variable called payload
  # .get_json() attached to request will extract JSON from request body 
  payload = request.get_json() 
  print(payload)
  new_member = models.Member.create(name=payload['name'], email=payload['email'], user=payload['user'])
  print(new_member) # this returns the id of the member 
  # if you check terminal you can see your body request like req.body 
  return "you hit member create route -- check terminal"

# peewee lets us interact with our database. 
# an object is a dictonary in Python 
# payload has the data you want to have 
# use the models field in yoru create 
# models.Member allows you take access 
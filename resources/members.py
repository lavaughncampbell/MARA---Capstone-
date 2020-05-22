# this file is similar to memberCon
import models


# blueprint is a way to create a self-contained grouping 
from flask import Blueprint, request, jsonify # import jsonify to define it. 
# request is --- data from clients is sent to the global request object 
# we can use this objet to get the json or form data or whatever 
# POST OR PUT requests have bodies

# this is a useful tool that comes with peewee. this is how we will convert
# our new member to a dictionary that will include all the fields from the database. 
from playhouse.shortcuts import model_to_dict



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
  result = models.Member.select() # query 



  print('result of member')
  print(result)

  # create new list 
  # for member in result:
  #   print(model_to_dict(member))
    # this loop gives you the members as dicts (objects) in the terminal 
  # use a loop to populate the list 
  # convert each model to a dict using model_to_dict 

  #OR 

  # use a list comprehension 
  member_dict = [model_to_dict(member) for member in result]
  print(member_dict)

  return jsonify({
    'data': member_dict, 
    'message': f"Successfully found {len(member_dict)} members",
    'status': 200
    }), 200
  # WORKS! THIS RETURNS ALL THE MEMBERS DICTS (OBJECTS) 
  # WE DONT WANT TO REALLY GET INTO A INDEX ROUTE BEFORE CREATE ROUTE 




















# ----------># ----------># ---------->
# CREATE

# POST /api/v1/members 
# SPECIFY THE HTTP METHOD 
# this is like app.posts 
@members.route('/', methods=['POST'])
def create_member():
  """creates a member in the database"""

  # request has a helpful method that will take data in a request 
  # and give it to us as JSON 
  # store this info in a variable called payload
  # .get_json() attached to request will extract JSON from request body 
  payload = request.get_json() 
  print(payload)
  new_member = models.Member.create(name=payload['name'], email=payload['email'], user=payload['user'])
  print(new_member) # this returns the id of the member -- check sqlite to see it. run sqlite3 members.sqlite
  # if you check terminal you can see your body request like req.body 

  print(new_member.__dict__) # this is when you print a dict. all my data is in there. 
   
                             # dict is a class attribute automatically added to python classes
  

  # you can't jsonify new member directly because its not a dictionary. it has a bunch of methods attached to it. 
  print(dir(new_member)) # look at all this model suff

  # we can use model_to_dict from playhouse (imported above -- playhouse === helpfule resource)
  member_dict = model_to_dict(new_member) # now we have something jsonifiable 
  # you get some meta data when you make a API request like "request successsful"
  # lets do some of that. 
  return jsonify(
    data=member_dict, 
    message='Successfully created member!', 
    status=201
    ), 201

 # THIS IS NOW LOOKING LIKE A REAL API. YOU TALK TO IT IN JSON IT TALKS BACK IN JSON 

# peewee lets us interact with our database. 
# an object is a dictonary in Python 
# payload has the data you want to have 
# use the models field in yoru create 
# models.Member allows you take access 
# send back the member we just created we will write a response to say it worked. 
# not serializable you can't just send back the new member

# for most things you can do member.__dict__ 


# ----------># ----------># ---------->
# DELETE 
@members.route('/<id>', methods=['DELETE']) # this is a decorator. Inside of it is the id specific to the member we want to delete and the method to DELETE.
def delete_member(id):
  # we are trying to delete the member with the id. 
  delete_query = models.Member.delete().where(models.Member.id == id)
  delete_query.execute()
  num_of_rows_deleted = delete_query.execute()
  print(num_of_rows_deleted)

  # todo: write logic -- if no rows were deleted return 
  # some message that delete didn't happen 
  return jsonify(
    data={},
    message="Successfully deleted {} with id {}".format(
      num_of_rows_deleted, id),
    status=200
  ), 200

  
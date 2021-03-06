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

from flask_login import current_user, login_required


# creating our blueprint
# first arg is blueprint name 
# second arg is its import name  
# similar to createing a router in express 
members = Blueprint('members', 'members')










# ----------># ----------># ---------->
# INDEX 

# GET /api/v1/members 
@members.route('/', methods=['GET'])
@login_required
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

  current_user_member_dicts = [model_to_dict(member) for member in current_user.members]

  for member_dict in current_user_member_dicts: 
    member_dict['user'].pop('password')

  print(current_user_member_dicts)

  return jsonify({
    'data': current_user_member_dicts, 
    'message': f"Successfully found {len(current_user_member_dicts)} members",
    'status': 200
    }), 200
  # WORKS! THIS RETURNS ALL THE MEMBERS DICTS (OBJECTS) 
  # WE DONT WANT TO REALLY GET INTO A INDEX ROUTE BEFORE CREATE ROUTE 




















# ----------># ----------># ---------->
# CREATE

# POST /api/v1/members 
# SPECIFY THE HTTP METHOD 
# this is like app.posts 
# We can now access the id of the currently logged in user
@members.route('/', methods=['POST'])
def create_member():
  """creates a member in the database"""

  # request has a helpful method that will take data in a request 
  # and give it to us as JSON 
  # store this info in a variable called payload
  # .get_json() attached to request will extract JSON from request body 
  payload = request.get_json() 
  print(payload)
  new_member = models.Member.create(
    name=payload['name'], 
    user=current_user.id, # using the logged in user to set this. if you are logged in the member created is associated with you 
    email=payload['email'] 
  )

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
  print(member_dict)
  member_dict['user'].pop('password') # remove password from user 

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

















# ----------># ----------># ---------->
# UPDATE
@members.route('/<id>', methods=['PUT'])
def update_member(id):
  payload = request.get_json()

  update_query = models.Member.update(
    name=payload['name'], 
    email=payload['email'],
    user=payload['user']
  ).where(models.Member.id == id) # specify where you want to update

  num_of_rows_modified = update_query.execute()

  #todo: we could do some better error checking here 
  
  # lets grab the updated member from database so we can include the 
  # modified member in the response we're sending back to the 
  # front end 

  updated_member = models.Member.get_by_id(id)
  updated_member_dict = model_to_dict(updated_member)

  return jsonify(
      data=updated_member_dict,
      message=f"Successfully updated dog with id {id}".format(id),
      status=200
    ), 200
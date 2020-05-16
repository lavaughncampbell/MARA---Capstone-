# this file is similar to memberCon
import models


# blueprint is a way to create a self-contained grouping 
from flask import Blueprint 

# creating our blueprint
# first arg is blueprint name 
# second arg is its import name  
# similar to createing a router in express 
members = Blueprint('members', 'members')


@members.route('/')
def members_index():
  return "members resource working"
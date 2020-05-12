


# <--------------- PEEWEE  ------------------>
# CREATE MODELS WITH PEEWEE 
# <--------------------------------------------> 
# import * means everything. 
# use peewee to create our models.
from peewee import *




# <--------------- DATETIME  ------------------>
# DATETIME TO FOR CREATED_AT VARIABLE IN TICKET
# <--------------------------------------------> 
# importing this for DateTimeField
import datetime 




# <--------------- FLASK_LOGIN  ------------------>
# FLASK_LOGIN MODULE TO SETUP AUTHENTICATION 
# <--------------------------------------------> 
# flask_login module to setup the user mode, sessions,
# logins, authentication. The user class model will inherit 
# from UserMixin 
from flask_login import UserMixin




# <--------------- SQLITE  ------------------>
# SQLITE DATABASE = STORE YOUR ENTIRE DATABASE IN ONE FILE 
# <--------------------------------------------> 
DATABASE = SqliteDatabase('mara.sqlite')




# <--------------- USER  ------------------>
# DEFINE USER MODEL 
# <--------------------------------------------> 
class User(UserMixin, Model): # all models must inherit from models
	email = CharField(unique=True)
	password = CharField()
	name = CharField()
	company = CharField()
	position = CharField()
	admin = Boolean()

	class Meta: 
		database = DATABASE




# <--------------- TEAM  ------------------>
# DEFINE TEAM MODEL 
# <--------------------------------------------> 
class Team(Model): # all models must inherit from models
	email = CharField()
	company = CharField()

	class Meta:
		database = DATABASE




# <--------------- PROJECT  ------------------>
# DEFINE PROJECT MODEL 
# <--------------------------------------------> 
class Project(Model): # all models must inherit from models
	name = CharField()
	description = CharField()
	team = ForeignKeyField(Team, backref='projects') #team who owns that project projects.team. backref for team.projects


	class Meta:
		database = DATABASE




# <--------------- TICKET  ------------------>
# DEFINE TICKET MODEL 
# <--------------------------------------------> 
class Ticket(Model): # all models must inherit from models
	title = CharField()
	description = CharField()
	priority = CharField()
	ticket_type = CharField()
	status = CharField()
	created_at = DateTimeField(default=datetime.now)
	project = ForeignKeyField(Project, backref='tickets') #project who owns that ticket ticket.project backref for project.ticket
	developer = ForeignKeyField(Developer, backref='tickets') #project who owns that ticket ticket.developer backref for developer.ticket

	class Meta:
		database = DATABASE



# <----------- DATBASE CONNECTION  -------------->
# INTIALIZE DATABASE CONNECTION  
# <--------------------------------------------> 
def initialize(): # method that will get called when the app starts
	DATABASE.connect()

	# create tables based on the model schemas. 
	DATABASE.create_tables([User, Team, Project, Ticket], safe=True)
	print("Connected to DB and created tables if they weren't already there")

	DATABASE.close() # close sql database connection. 

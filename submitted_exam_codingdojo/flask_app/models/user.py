# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import tree

from flask_app import app
from flask_bcrypt import Bcrypt   
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
        # which is made by invoking the function Bcrypt with our app as an argument
        
import re	# the regex module

class User: # model the class after the user table from our database
    
    db='tree' #login database (in mySQL workbench)

    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
        self.trees=[] # one to many
        self.status = False
        


# ADDED
    @classmethod
    def add_to_user_visitors( cls , data ): #data comes from controller_ninjas.py in /create_ninja route
        query = "INSERT INTO visitor ( user_id , tree_id ) VALUES (%(user_id)s, %(tree_id)s);"
        return connectToMySQL(cls.db).query_db(query,data) #tablename or database name??

    @classmethod
    def delete_user_visitors( cls , data ): #data comes from controller_ninjas.py in /create_ninja route
        query = "DELETE FROM visitor WHERE (user_id = %(user_id)s AND tree_id = %(tree_id)s);"
        return connectToMySQL(cls.db).query_db(query,data) #tablename or database name??

    # @classmethod
    # def get_user_with_skeptic_sightings( cls , data ):
    #     query = "SELECT * FROM user LEFT JOIN skeptic ON skeptic.user_id = user.id LEFT JOIN sighting ON skeptic.sighting_id = sighting.id WHERE user.id = %(id)s;"
    #     results = connectToMySQL(cls.db).query_db( query , data )
    #     # results will be a list of author objects with the book attached to each row. 
    #     user = cls( results[0] )
    #     for row_from_db in results:
    #         # Now we parse the author data to make instances of authors and add them into our list.
    #         sighting_data = {
    #         "id" : row_from_db["sighting.id"],
    #         "location" : row_from_db["location"],
    #         "what_happened" : row_from_db["what_happened"],
    #         "number" : row_from_db["number"],
    #         "created_at" : row_from_db["sighting.created_at"],
    #         "updated_at" : row_from_db["sighting.updated_at"]
    #         }
    #         user.sightings.append( sighting.Sighting( sighting_data ) )   #appends book instances to list of books in author  
    #     return user #returns dictionary: one author with a list of books


# def add_skeptic_user
# data = {"user_id" : request.form["user_id"],
# "sighting_id": id
# }
# User.add_to_user_skeptics(data)

#vs






# REGISTRATION
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO user ( first_name , last_name  , email, password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s ,NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        result = connectToMySQL(cls.db).query_db( query, data )  # returns an ID because of insert statement
        return result
    

#LOGIN
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
            #result is a list of dictionaries
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0]) 

    @staticmethod
    def validate_user(user):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        is_valid = True # we assume this is true

        currentUser = User.get_by_email({'email':user['email']})
        if currentUser: #falsy/truthy -> get_by_email returns either empty tuple or a tuple if it already exists
            flash("User already exists")
            is_valid = False
        if len(user['fname']) < 2:
            flash("First name is required.")
            is_valid = False
        if len(user['lname']) < 2:
            flash("Last name is required.")
            is_valid = False
        if len(user['email']) < 1:
            flash("Email is required.")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password should be a minimum of 8 characters.")
            is_valid = False
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False

        return is_valid


    @staticmethod
    def validate_login(user):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        is_valid = True # we assume this is true
        if len(user['email']) < 1:
            flash("Email is required.")
            is_valid = False
        if len(user['password']) < 1:
            flash("Password is required.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid




# Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM user;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []      # Create an empty list to append our instances of users
        for user in results: # Iterate over the db results and create instances of users with cls.
            users.append( cls(user) )
        return users #returns list of class objects (list of dictionaries)
            

    @classmethod
    def get_one(cls, data):
        # data = {'id': id}
        query = "SELECT * FROM user WHERE id = %(id)s ;" #%(id)s is the key of the dictionary data and returns id
        results = connectToMySQL(cls.db).query_db(query, data) #query_db returns list of objects
        print ("here",results)
        return cls(results[0])   

    # class method to remove one user from the database
    @classmethod
    def delete(cls, data ):
        query = "DELETE FROM user WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db( query, data )

    # class method to edit one user in the database
    @classmethod
    def update(cls, data ):
        query = "UPDATE user SET first_name = %(fname)s , last_name = %(lname)s  , email = %(email)s , updated_at=NOW() WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db( query, data )

    @classmethod
    def get_user_with_trees( cls , data ):
        query = "SELECT * FROM user LEFT JOIN tree ON tree.user_id = user.id WHERE user.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db( query , data )
        # results will be a list of topping objects with the ninja attached to each row. 
        user = cls( results[0] )
        for row_from_db in results:
            # Now we parse the ninja data to make instances of ninjas and add them into our list.
            tree_data = {
                "id" : row_from_db["tree.id"],  #ninjas.__ because id overlaps with id in dojo
                "species" : row_from_db["species"],
                "location" : row_from_db["location"],
                "reason" : row_from_db["reason"],
                "user_id" : row_from_db['user_id'],
                "created_at" : row_from_db["tree.created_at"],
                "updated_at" : row_from_db["tree.updated_at"]
                
            }
            user.trees.append( tree.Tree( tree_data ) )
        return user     #returns an object with a list of posts inside 
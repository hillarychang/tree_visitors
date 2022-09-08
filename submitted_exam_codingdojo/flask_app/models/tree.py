# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


from flask_app import app
from flask_bcrypt import Bcrypt   
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
        # which is made by invoking the function Bcrypt with our app as an argument
        
import re	# the regex module

class Tree: # model the class after the user table from our database
    
    db='tree' #login database (in mySQL workbench)

    def __init__( self , data ):
        self.id = data['id']
        self.species = data['species']
        self.location = data['location']
        self.reason = data['reason']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']   #should i have this here??? yes. its a hidden input 

        self.visitedUsers = [] # use this to determine if the user is a skeptic (many to many)
        
        self.numVisit = 0

        self.planter = {"first_name" : "",
                "last_name" : ""
            }


    # @classmethod
    def amtVisitors(self):
        return len(self.visitedUsers)

    @classmethod
    def findPlanterById(cls, data):
        query = """
            SELECT tree.*, user.first_name, user.last_name  
            FROM tree 
            JOIN user ON tree.user_id = user.id 
            WHERE tree.id = %(tree_id)s;
            """
        results = connectToMySQL(cls.db).query_db( query , data )
        # results will be a list of author objects with the book attached to each row. 
        output = cls( results[0] )
        for row_from_db in results:
            
            # Now we parse the author data to make instances of authors and add them into our list.
            join_data = {
                "first_name" : row_from_db["first_name"],
                "last_name" : row_from_db["last_name"]
            }
            output.planter = ( join_data ) 

        return output #^get a list of users for that sighting that are skeptical 



    def validate_tree(sighting):
        is_valid = True # we assume this is true
        if len(sighting['location']) < 1:
            flash("Location must not be blank.")
            is_valid = False
        if len(sighting['reason']) < 1:
            flash("Reason must not be blank.")
            is_valid = False
        if len(sighting['species']) < 1:
            flash("Species must not be blank.")
            is_valid = False
        return is_valid





    # This method will retrieve the book with all the authors that are associated with the book.
    @classmethod
    def get_trees_with_visitors( cls , data ):
        query = """
            SELECT * 
            FROM tree 
            LEFT JOIN visitor ON visitor.tree_id = tree.id 
            LEFT JOIN user ON visitor.user_id = user.id 
            WHERE tree.id = %(id)s;
            """
        results = connectToMySQL(cls.db).query_db( query , data )
        # results will be a list of author objects with the book attached to each row. 
        tree = cls( results[0] )

        # count=0
        for row_from_db in results:
            # count += 1
            # Now we parse the author data to make instances of authors and add them into our list.
            user_data = {
                "id" : row_from_db["user.id"],
                "first_name" : row_from_db["first_name"],
                "last_name" : row_from_db["last_name"],
                "email" : row_from_db["email"],

                "password":row_from_db["password"],

                "created_at" : row_from_db["user.created_at"],
                "updated_at" : row_from_db["user.updated_at"]
            }
            tree.visitedUsers.append(user.User( user_data ) )
        tree.numVisit = len(tree.visitedUsers)

        # tree.amtVisitors = count
            #created list of visitors for specific tree

        return tree #^get a list of users for that sighting that are skeptical 





    @classmethod
    def save(cls, data ):
        query = "INSERT INTO tree ( species , location, reason, user_id, created_at , updated_at ) VALUES ( %(species)s , %(location)s, %(reason)s, %(user_id)s , %(created_at)s , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        result = connectToMySQL(cls.db).query_db( query, data )  # returns an ID because of insert statement
        return result
    
    # class method to remove one user from the database
    @classmethod
    def delete(cls, data ):
        query = "DELETE FROM tree WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db( query, data )

    


    # Now we use class methods to query our database
    @classmethod
    def checkStatus(cls, data):

        #*changed this method
        query = "SELECT * FROM visitor WHERE (user_id = %(user_id)s AND tree_id = %(tree_id)s);"

        results = connectToMySQL(cls.db).query_db(query, data) #results returns a list of dictionaries (key is column, value is row in specific column)
        

        var = None
        print("length",len(results))
        if len(results) == 1:
            var = True
        else:
            var = False

        return var #returns list of class objects (list of dictionaries)



    @classmethod
    def getAmtVisitor(cls, data):

        #*changed this method
        query = "SELECT * FROM visitor WHERE tree_id = %(tree_id)s;"

        results = connectToMySQL(cls.db).query_db(query, data) #results returns a list of dictionaries (key is column, value is row in specific column)
        
        return len(results)

        # var = None
        # print("length",len(results))
        # if len(results) == 1:
        #     var = True
        # else:
        #     var = False

        # return var #returns list of class objects (list of dictionaries)


# Now we use class methods to query our database
    @classmethod
    def get_all(cls):

        #*changed this method
        query = "SELECT * FROM tree LEFT JOIN user ON tree.user_id = user.id;"

        results = connectToMySQL(cls.db).query_db(query)
        
        trees = []      # Create an empty list to append our instances of users
        
        print("RESULTS",results)
        for tree in results: # Iterate over the db results and create instances of users with cls.
            one_tree = cls(tree)


            user_data = {
                "id":tree["user.id"], 
                "first_name":tree["first_name"], 
                "last_name":tree["last_name"],
                "email":tree["email"],
                "password":tree["password"],
                "created_at" :tree['user.created_at'],
                "updated_at": tree['user.updated_at']
            }

            one_tree.user = user.User(user_data)
            trees.append( one_tree)
        return trees #returns list of class objects (list of dictionaries)



    


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM tree WHERE id = %(id)s ;" #%(id)s is the key of the dictionary data and returns id
        results = connectToMySQL(cls.db).query_db(query, data) #query_db returns list of objects
        return cls(results[0])   


    # if logged in as user, can delete post
    @classmethod
    def delete(cls, data ):
        query = "DELETE FROM tree WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db( query, data )

    # class method to edit one user in the database
    @classmethod
    def update(cls, data ):
        query = "UPDATE tree SET species = %(species)s, location = %(location)s, reason =  %(reason)s, created_at =%(created_at)s, updated_at=NOW() WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db( query, data )
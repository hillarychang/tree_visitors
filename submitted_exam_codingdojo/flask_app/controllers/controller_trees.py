from flask import render_template, redirect, request, session, flash

from flask_app import app

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_app.models.tree import Tree
from flask_app.models.user import User

app.secret_key = "shhh"



@app.route("/show_tree_users/<int:id>")  #ID comes from -> check index.html route
def show_tree_users(id):
    data = {"id":id}
    one_tree = Tree.get_one(data)
    current_user = User.get_one({'id':session['user_id']})

    status = Tree.checkStatus({"user_id":session['user_id'], "tree_id":id})
    # print("status",status)


    tree_with_users = Tree.get_trees_with_visitors(data) #[sighting.PY]gives one specific sighting

    return render_template("view_tree.html", curr_status = status, tree_user = tree_with_users, tree = one_tree, users = current_user)


# @app.route("/show/<int:id>") #runs show-one-user page
# def show_one(id):
#     data = {'id':id}
#     sightings = Sighting.get_one(data)

#     user_data = {"id":session['user_id']} # need user's id
#     user = User.get_one(user_data)

#     another_user = User.get_one({'id':sightings.user_id})

#     return render_template("view_sighting.html", one_sighting = sightings, users = user, other_user = another_user)




@app.route("/tree") #runs add tree form
def tree():
    
    trees = Tree.get_all()
    data = {"id":session['user_id']} # need user's id
    # user = User.get_user_with_recipes(data) #returns a user with a list of posts

    #ADDED
    user = User.get_user_with_trees(data) #returns a user with a list of recipes
    return render_template("add_tree.html", all_trees = trees, users = user) 






#route to update
@app.route("/update/<int:id>", methods=["POST"]) #deletes a user, doesn't run a page??
def update_tree(id):

    if not Tree.validate_tree(request.form): #request.form  (check user.py)
        return redirect('/update/<int:id>')

    data = {
        'id':id,
        "species": request.form["species"],
        "location" : request.form["location"],
        "reason" : request.form["reason"],
        "created_at" : request.form["created_at"]

    }

    Tree.update(data)
    return redirect('/showUser')
    # return redirect(f'/show/{id}')


@app.route("/edit/<int:id>") #update a user, runs edit page
def edit_tree(id):

    data = {'id':id}
    trees = Tree.get_one(data)
    user = User.get_user_with_trees({'id':trees.user_id}) #returns a user with a list of recipes

    return render_template("edit_tree.html", tree = trees, users  = user)






@app.route('/create_tree', methods=["POST"])
def create_tree():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    
    if not Tree.validate_tree(request.form): #request.form  (check user.py)
        return redirect('/create_tree') #???

    
    data = {

            "species" : request.form["species"],
            "location" : request.form["location"],
            "reason" : request.form["reason"],
            "user_id": session['user_id'],
            "created_at": request.form["created_at"] #added this

    }
    # We pass the data dictionary into the save method from the Nina class.
    id = Tree.save(data)
    return redirect('/showUser') 



@app.route("/delete/<int:id>") #deletes a user, doesn't run a page??
def delete_tree(id):
    data = {'id':id}
    Tree.delete(data)
    return redirect('/showUser')
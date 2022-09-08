from flask import render_template, redirect, request, session, flash

from flask_app import app

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_app.models.user import User
from flask_app.models.tree import Tree

app.secret_key = "shhh"


# controller_authors:add_favorite_author -> show_book_authors
# show_book_authors



# @app.route("/delete_visitor/<int:id>") #runs add recipe form
# def delete_visitor(id):
#     data = {
#     "user_id":session['user_id'],
#     "tree_id": id
#     } 

#     user = User.get_one({"id":session['user_id']})


#     tree = Tree.get_trees_with_visitors({'id':id}) #[sighting.PY]gives one specific sighting

#     User.delete_user_visitors(data)  
#     return redirect(f'/show_tree_users/{id}') #redirect goes to route, render_template shows html page


@app.route("/showOne") #runs starting form
def showOne():
    
    data = {"id":session['user_id']} # need user's id
    user = User.get_user_with_trees(data) #returns a user with a list of recipes
    print("HERE",user.trees)
    return render_template("one_user.html", users = user) 




@app.route("/create_visitor/<int:id>") #runs add recipe form
def create_visitor(id):
    data = {
    "user_id":session['user_id'],
    "tree_id": id
    } 

    user = User.get_one({"id":session['user_id']})


    tree = Tree.get_trees_with_visitors({'id':id}) #[sighting.PY]gives one specific sighting
    print("NOWHERE")
#inserts into table visitor
    User.add_to_user_visitors(data)  

                
    #inset into skeptic
    return redirect(f'/show_tree_users/{id}') #redirect goes to route, render_template shows html page



# REGISTRATION
@app.route('/create_user', methods=['POST'])
def create_user():

    if not User.validate_user(request.form): #request.form  (check user.py)
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "first_name": request.form['fname'],
        "last_name": request.form['lname'],
        "email": request.form['email'],
        "password" : pw_hash #assign hash to self.password
    }

    user_id = User.save(data)

    print("ID",user_id)
    # store user id into session
    session['user_id'] = user_id
    return redirect("/showUser")



# LOGIN
@app.route('/login', methods=['POST'])
def login():

    if not User.validate_login(request.form): #request.form  (check user.py)
        return redirect('/')


    data = { "email" : request.form["email"] }

    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')

    session['user_id'] = user_in_db.id #create session with user_in_db.id 

    return redirect("/showUser")


# @app.route("/showUser") #runs starting form
# def showUser():
    
#     trees = Tree.get_all()
#     data = {"id":session['user_id']} # need user's id
#     user = User.get_user_with_trees(data) #returns a user with a list of trees
    
#     # len(.visitedUsers)

#     # findPlanterById({"tree_id":})
#     len()
#     # amtVisit = Tree.getAmtVisitor({"tree_id":id})
#     # print("amtVisit",amtVisit)

#     return redirect("/showUser") 


@app.route("/showUser") #runs starting form
def showUser():
    
    trees = Tree.get_all()
    data = {"id":session['user_id']} # need user's id
    user = User.get_user_with_trees(data) #returns a user with a list of trees
    
    # len(.visitedUsers)

    # findPlanterById({"tree_id":})
    # len()


    # amtVisit = Tree.getAmtVisitor({"tree_id":id})
    # print("amtVisit",amtVisit)


    return render_template("result.html", all_trees = trees, users = user) 



# CORRECT FOR RESULT.HTML
# @app.route("/showUser/<int:id>") #runs starting form
# def showUser():
    
#     trees = Tree.get_all()
#     data = {"id":session['user_id']} # need user's id
#     user = User.get_user_with_trees(data) #returns a user with a list of recipes
    
#     planter = Tree.findPlanterById({"tree_id":id})

#     return render_template("result.html", the_planter = planter, all_trees = trees, users = user) 





@app.route("/") #runs starting form
def index():
    return render_template("index.html") 



@app.route("/log_out") 
def log_out():
    session.clear()
    return redirect('/')



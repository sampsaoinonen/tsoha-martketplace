from app import app
from flask import render_template, request, redirect, flash
import users

@app.route("/")     
def index():        
    user_id = users.user_id()    
    return render_template("index.html", user_id=user_id)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            flash("Wrong password or user doesn't exists!")
            return redirect("/login")            

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"]) 
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            flash("Passwords don't mach!")
            return redirect("/register")
        if len(password1) < 5 or len(password1) > 20:
            flash("Password has to be between 5 and 20 characters!")
            return redirect("/register")
        if len(username) < 3 or len(password1) > 20:
            flash("Username has to be between 3 and 20 characters!")
            return redirect("/register")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", error="Something went wrong. Registration was aborted!")

@app.route("/new_ad", methods=["GET", "POST"]) 
def new_ad():
    if request.method == "GET":
        return render_template("new_ad.html")
    if request.method == "POST":
        users.check_csrf(request.form["csrf_token"])
        title = request.form["title"]
        description = request.form["description"]
        phone = request.form["phone"]
        email = request.form["email"]
        location = request.form["location"]
        price = request.form["price"]        
        if len(title) < 3 or len(password1) > 20:
            flash("Title has to be between 5 and 20 characters!")
            return redirect("/new_ad")
        if len(description) < 3 or len(description) > 200:
            flash("Username has to be between 3 and 200 characters!")
            return redirect("/new_ad")
        if len(phone) > 20:
            flash("Phone number has to be under 20 characters!")
            return redirect("/new_ad")
        if len(email) > 50:
            flash("Email address has to be under 20 characters!")
            return redirect("/new_ad")
        if len(location) > 50:
            flash("Location has to be under 50 characters!")
            return redirect("/new_ad")
        if len(price) < 0 or len(price) > 9999999.99 :
            flash("Price has to be between 0 and 9,999,999.99")
            return redirect("/new_ad")

        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", error="Something went wrong. Registration was aborted!")
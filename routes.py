from app import app
from flask import render_template, request, redirect, flash
import users, ads, images, messages, comments, validators
import datetime

@app.route("/")     
def index():            
    user_id = users.user_id()
    unread = messages.check_unread(user_id)
    return render_template("index.html", unread=unread)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            flash("Login succesful!", "success")
            return redirect("/")
        else:
            flash("Wrong password or user doesn't exist!", "error")
            return redirect("/login")            

@app.route("/logout")
def logout():
    users.logout()
    flash("You have logged out!", "success")
    return redirect("/")

@app.route("/register", methods=["GET", "POST"]) 
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if not validators.register(username, password1, password2):
            return redirect("/register")       
        if users.register(username, password1):
            flash("Registration succesful!", "success")
            return redirect("/")
        else:
            flash("Registration not succesful! Your username might be already in use.", "error")
            return redirect("/register")

@app.route("/browse")
def browse():
    all_ads = ads.get_ads()
    user_id = users.user_id()
    unread = messages.check_unread(user_id)
    return render_template("ads.html", all_ads=all_ads, unread=unread)

@app.route("/new_ad", methods=["GET", "POST"]) 
def new_ad():
    user_id = users.user_id()
    if user_id == 0:
        flash("Log in to create a new ad!")
        return redirect("/login")
    unread = messages.check_unread(user_id)
    form = request.form
    categories = ads.get_cats()
    types = ads.get_types()
    if request.method == "GET":        
        return render_template("new_ad.html", categories=categories, types=types, unread=unread)
    if request.method == "POST":
        users.check_csrf(request.form["csrf_token"])     
        cat_id = request.form["cate"]        
        title = request.form["title"]
        description = request.form["description"]
        phone = request.form["phone"]
        email = request.form["email"]
        location = request.form["location"]
        type_id = request.form["type"]
        price = request.form["price"]
        expires = request.form["expires"]
        if not validators.new_ad(title, description, phone, email, location, price, expires, cat_id, type_id):        
            return render_template("new_ad.html", form=form, categories=categories, types=types, unread=unread)
        ad_id = ads.add_ad(title, description, phone, email, location, price, expires, user_id, cat_id, type_id)
        file = request.files["file"]             
        if file:
            data = file.read()
            image_name = file.filename         
            if not validators.image(image_name, len(data)):
                return render_template("new_ad.html", form=form, categories=categories, types=types, unread=unread)                                                
            images.add_ad_image(image_name, ad_id, data)
        return redirect("/browse")
    
@app.route("/ad/<int:ad_id>")
def ad(ad_id):
    user_id = users.user_id()
    unread = messages.check_unread(user_id)
    ad = ads.get_ad(ad_id)
    expires_date = ad[8] + datetime.timedelta(days=10)
    ad_comments = comments.get_ad_comments(ad_id)
    is_image = images.check_ad_image(ad_id)
    return render_template("ad.html", ad=ad, expires_date=expires_date, is_image=is_image, ad_comments=ad_comments, unread=unread)

@app.route("/ad/<int:ad_id>/edit", methods=["GET", "POST"])
def edit_ad(ad_id):
    user_id = users.user_id()
    unread = messages.check_unread(user_id)
    categories = ads.get_cats()
    types = ads.get_types()
    if request.method == "GET":
        ad = ads.get_ad(ad_id)        
        return render_template("new_ad.html", form=ad, categories=categories, types=types, unread=unread)
    if request.method == "POST":
        form = request.form
        users.check_csrf(request.form["csrf_token"])
        cat_id = request.form["cate"]        
        title = request.form["title"]
        description = request.form["description"]
        phone = request.form["phone"]
        email = request.form["email"]
        location = request.form["location"]
        type_id = request.form["type"]
        price = request.form["price"]
        expires = request.form["expires"]
        if not validators.new_ad(title, description, phone, email, location, price, expires):        
            return render_template("new_ad.html", form=form, categories=categories, types=types, unread=unread)
        ads.update_ad(ad_id, title, description, phone, email, location, price, expires, user_id, cat_id, type_id)
        file = request.files["file"]             
        if file:
            data = file.read()
            image_name = file.filename         
            if not validators.image(image_name, len(data)):
                return render_template("new_ad.html", form=form, categories=categories, types=types, unread=unread)                                                
            images.delete_ad_image(ad_id)
            images.add_ad_image(image_name, ad_id, data)
        return redirect("/ad/<int:ad_id>")

@app.route("/ad/<int:ad_id>/delete")
def delete_ad(ad_id):
    user_id = users.user_id()
    ads.delete_ad(user_id, ad_id)
    if not ads.get_ad(ad_id):
        flash("Ad deleted succesfully!", "success")
        return redirect("/browse")
    flash("You don't have the rights to delete this ad!", "error")
    return redirect("/ad/<int:ad_id>")

@app.route("/add_ad_comment", methods=["POST"])
def add_ad_comment():
    user_id = users.user_id()
    if user_id == 0:
        flash("Log in to leave a comment!")
        return redirect("/login")
    users.check_csrf(request.form["csrf_token"])
    content = request.form["content"]
    ad_id = request.form["ad_id"]
    if validators.add_comment(content):
        comments.add_ad_comment(content, ad_id, user_id)
        flash("Your comment has been added!", "success")
    return redirect("/ad/" + ad_id)

@app.route("/ad_comment/delete", methods=["POST"])
def delete_ad_comment():
    user_id = users.user_id()
    if request.method == "POST":
        users.check_csrf(request.form["csrf_token"])
        ad_comment_id = request.form["comment_id"]
        ad_id = request.form["ad_id"]        
        comments.delete_ad_comment(user_id, ad_comment_id)    
        if not comments.check_ad_comment(ad_comment_id):                   
            flash("Comment deleted succesfully!", "success")                
        else:
            flash("You have no permission to delete this comment!", "error")
    return redirect("/ad/" + ad_id) 


@app.route("/new_message",methods=["GET", "POST"])
def new_messsage():     
    user_id = users.user_id()
    if user_id == 0:
        flash("Log in to send a new message!", "error")
        return redirect("/login")
    unread = messages.check_unread(user_id)
    form = request.form
    if request.method == "GET":
        return render_template("new_message.html", unread=unread)
    if request.method == "POST":
        users.check_csrf(request.form["csrf_token"])        
        user_to_name = request.form["user_to"]    
        subject = request.form["subject"]
        message = request.form["message"]
        if users.search(user_to_name):
            if not validators.new_message(subject, message):
                return render_template("new_message.html", form=form, unread=unread)
            user_to_id = users.search(user_to_name)
            messages.send(user_id, user_to_id, subject, message) 
            flash("The message has been sent!", "success")
            return redirect("/sent")            
        else:            
            flash("The user doesn't exist!", "error")
            return render_template("new_message.html", form=form, unread=unread)

@app.route("/new_message/<user_to>/<subject>")
def ad_message(user_to, subject):
    user_id = users.user_id()
    if user_id == 0:
        flash("Log in to create a new ad!", "error")
        return redirect("/login")
    unread = messages.check_unread(user_id)
    form = {}
    form["user_to"] = user_to
    form["subject"] = subject
    return render_template("new_message.html", form=form, unread=unread)


@app.route("/inbox")
def inbox():
    user_id = users.user_id()
    if user_id == 0:
        flash("Log in to create a new ad!", "error")
        return redirect("/login")
    unread = messages.check_unread(user_id)
    msgs = messages.get_inbox(user_id)
    return render_template("inbox.html", msgs=msgs, unread=unread)

@app.route("/inbox/<int:msg_id>")
def inbox_one(msg_id):
    user_id = users.user_id()
    if user_id == 0:
        flash("Log in to create a new ad!", "error")
        return redirect("/login")
    unread = messages.check_unread(user_id)
    msg = messages.get_one_inbox(user_id, msg_id)
    messages.seen(msg_id)
    return render_template("message.html", msg=msg, unread=unread)

@app.route("/sent")
def sent():
    user_id = users.user_id()
    if user_id == 0:
        flash("Log in to create a new ad!")
        return redirect("/login")
    unread = messages.check_unread(user_id)
    msgs = messages.get_sent(user_id)
    return render_template("sent.html", msgs=msgs, unread=unread)

@app.route("/sent/<int:msg_id>")
def sent_one(msg_id):
    user_id = users.user_id()
    if user_id == 0:
        flash("Log in to create a new ad!", "error")
        return redirect("/login")
    unread = messages.check_unread(user_id)
    msg = messages.get_one_sent(user_id, msg_id)
    messages.seen(msg_id)
    return render_template("message.html", msg=msg, unread=unread)

@app.route("/search")
def search():
    user_id = users.user_id()
    unread = messages.check_unread(user_id)
    categories = ads.get_cats()
    types = ads.get_types()
    return render_template("search.html", unread=unread, categories=categories, types=types)

@app.route("/search_result")
def search_result():    
    user_id = users.user_id()
    if user_id != 0:
        users.check_csrf(request.args["csrf_token"])
    unread = messages.check_unread(user_id)
    username = request.args["user"].lower()
    cat_id = request.args["cate"]
    title = request.args["title"].lower()
    description = request.args["description"].lower()
    price_low = request.args["price_low"]
    price_high = request.args["price_high"]
    type_id = request.args["type"]
    if not validators.search(username, title, description, price_low, price_high):
        return redirect("/search")
    results = ads.search(username, title, description, price_low, price_high, cat_id, type_id)
    return render_template("ads.html", all_ads=results, unread=unread)

@app.route("/search_profile")
def search_profile():
    user_id = users.user_id()
    unread = messages.check_unread(user_id)    
    return render_template("search_profile.html", unread=unread)

@app.route("/search_profile_result")
def search_profile_result():    
    user_id = users.user_id()
    if user_id != 0:
        users.check_csrf(request.args["csrf_token"])
    unread = messages.check_unread(user_id)
    username = request.args["user"].lower()    
    admin = request.args["admin"]
    if not validators.search_profile(username):
        return redirect("/search_profile")
    results = users.search_profile(username, admin)
    return render_template("profiles.html", results=results, unread=unread)

@app.route("/profile/<int:profile_id>")
def profile(profile_id):
    user_id = users.user_id()
    unread = messages.check_unread(user_id)
    profile = users.get_profile(profile_id)
    user_comments = comments.get_user_comments(profile_id)
    is_image = images.check_user_image(profile_id)
    return render_template("profile.html", profile=profile, user_comments=user_comments, is_image=is_image, unread=unread)

@app.route("/add_user_comment", methods=["POST"])
def add_user_comment():
    user_id = users.user_id()
    if user_id == 0:
        flash("Log in to leave a comment!")
        return redirect("/login")
    users.check_csrf(request.form["csrf_token"])
    content = request.form["content"]
    profile_id = request.form["profile_id"]
    if validators.add_comment(content):
        comments.add_user_comment(content, user_id, profile_id)
        flash("Your comment has been added!", "success")
    return redirect("/profile/" + profile_id)

@app.route("/user_comment/delete", methods=["POST"])
def delete_user_comment():
    user_id = users.user_id()
    if request.method == "POST":
        users.check_csrf(request.form["csrf_token"])
        user_comment_id = request.form["user_comment_id"]
        profile_id = request.form["profile_id"]        
        comments.delete_user_comment(user_id, user_comment_id)    
        if not comments.check_ad_comment(user_comment_id):                   
            flash("Comment deleted succesfully!", "success")                
        else:
            flash("You have no permission to delete this comment!", "error")
    return redirect("/profile/" + profile_id) 


@app.route("/profile/<int:profile_id>/edit_profile", methods=["GET", "POST"])
def edit_profile(profile_id):
    user_id = users.user_id()
    if user_id == 0:
        flash("Log in to edit your profile!")
        return redirect("/login")
    unread = messages.check_unread(user_id)
    profile = users.get_profile(profile_id)
    if request.method == "GET":        
        return render_template("edit_profile.html", profile=profile, unread=unread)
    if request.method == "POST":
        users.check_csrf(request.form["csrf_token"])
        description = request.form["description"]
        file = request.files["file"]
        if validators.update_description(description):
            users.update_description(description, user_id, profile_id)
        if file:
            data = file.read()
            image_name = file.filename         
            if not validators.image(image_name, len(data)):
                return redirect("/")
            if images.check_user_image(user_id):
                images.delete_user_image(user_id)
            images.add_user_image(image_name, user_id, data)
        return redirect("/profile/" + str(user_id))

@app.route("/profile/<int:profile_id>/delete")
def delete_profile(profile_id):
    user_id = users.user_id()
    users.delete_user(user_id, profile_id)    
    if not users.get_profile(profile_id):
        if user_id == profile_id:
            users.logout()                
        flash("Profile deleted succesfully!", "success")        
        return redirect("/")
    flash("You have no permission to delete this profile!", "error")
    return redirect("/")

@app.route("/image/<int:ad_id>")
def show_image(ad_id):    
    image = images.get_ad_image(ad_id)
    if image:
        return image
    flash("Image could not been found")
    return redirect("/")

@app.route("/user_image/<int:user_id>")
def show_user_image(user_id):    
    image = images.get_user_image(user_id)
    if image:
        return image
    flash("Image could not been found")
    return redirect("/")
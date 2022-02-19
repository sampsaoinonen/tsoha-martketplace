from app import app
from flask import render_template, request, redirect, flash
import users, ads, images, db, messages
import datetime

@app.route("/")     
def index():            
    user_id = users.user_id()
    unread = messages.check_unread(user_id)
    return render_template("index.html", user_id=user_id, unread=unread)

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
            flash("Wrong password or user doesn't exist!")
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
        if len(username) < 3 or len(username) > 20:
            flash("Username has to be between 3 and 20 characters!")
            return redirect("/register")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", error="Something went wrong. Registration was aborted!")

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
    if request.method == "GET":
        categories = ads.get_cats()
        types = ads.get_types()
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
        
        if len(title) < 3 or len(title) > 30:
            flash("Title has to be between 3 and 30 characters!")
            return redirect("/new_ad")
        if len(description) < 3 or len(description) > 200:
            flash("Description has to be between 3 and 200 characters!")
            return redirect("/new_ad")
        if len(phone) > 20:
            flash("Phone number has to be at most 20 characters!")
            return redirect("/new_ad")
        if len(email) > 50:
            flash("Email address has to be at most 20 characters!")
            return redirect("/new_ad")
        if len(location) > 50:
            flash("Location has to be at most 50 characters!")
            return redirect("/new_ad")
        if len(price) < 0 or len(price) > 9999999.99 :
            flash("Price has to be between 0 and 9,999,999.99")
            return redirect("/new_ad")
        if len(expires) < 1 or len(expires) > 365 :
            flash("Number of days have to be between 1 and 365")
            return redirect("/new_ad")
        
        ad_id = ads.add_ad(title, description, phone, email, location, price, expires, user_id, cat_id, type_id)

        file = request.files["file"]
        image_name = file.filename
        if file:
            if not image_name.endswith(".jpg"):
                flash("Invalid filetype!")
                return redirect("/new_ad")
            data = file.read()        
            if len(data) > 1000*1024:
                flash("Your image is too big!")
                return redirect("/new_ad")
            images.add_adimage(image_name, ad_id, data)
        return redirect("/browse")
    
@app.route("/ad/<int:ad_id>")
def ad(ad_id):
    user_id = users.user_id()
    unread = messages.check_unread(user_id)
    ad = ads.get_ad(ad_id)
    expires_date = ad[8] + datetime.timedelta(days=10)
    is_image = images.check_adimage(ad_id)
    return render_template("ad.html", ad=ad, expires_date=expires_date, is_image=is_image, unread=unread)

@app.route("/image/<int:ad_id>")
def show_image(ad_id):    
    image = images.get_adimage(ad_id)
    if image:
        return image
    flash("Image could not been found")
    return redirect('/')

@app.route("/new_message",methods=["GET", "POST"])
def new_messsage():     
    user_id = users.user_id()
    if user_id == 0:
        flash("Log in to create a new ad!")
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
            user_to_id = users.search(user_to_name)
            messages.send(user_id, user_to_id, subject, message) #here redirect to inbox
            flash("The message has been sent!")
            return redirect("/sent")            
        else:            
            flash("The user doesn't exist!")
            return render_template("new_message.html", form=form, unread=unread)

@app.route("/inbox")
def inbox():
    user_id = users.user_id()
    if user_id == 0:
        flash("Log in to create a new ad!")
        return redirect("/login")
    unread = messages.check_unread(user_id)
    msgs = messages.get_inbox(user_id)
    return render_template("inbox.html", msgs=msgs, unread=unread)

@app.route("/inbox/<int:msg_id>")
def inbox_one(msg_id):
    user_id = users.user_id()
    if user_id == 0:
        flash("Log in to create a new ad!")
        return redirect("/login")
    unread = messages.check_unread(user_id)
    msg = messages.get_one_inbox(user_id, msg_id)
    messages.seen(msg_id)
    return render_template("inbox_one.html", msg=msg, unread=unread)

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
        flash("Log in to create a new ad!")
        return redirect("/login")
    unread = messages.check_unread(user_id)
    msg = messages.get_one_sent(user_id, msg_id)
    messages.seen(msg_id)
    return render_template("sent_one.html", msg=msg, unread=unread)


@app.route("/new_message/<int:user_to>", methods=["POST"]) ### not usefull atm
def direct_message(user_to):
    user_to = request.form["user_to"]
    if not users.search(user_to):
        flash("The user doesn't exist!")
        return redirect("new_message.html")
    return render_template("direct_message.html", user_to=user_to)

@app.route("/search")
def search():
    user_id = users.user_id()
    unread = messages.check_unread(user_id)
    return render_template("search.html", unread=unread)

@app.route("/search_result")
def search_result():    
    user_id = users.user_id()
    if user_id != 0:
        users.check_csrf(request.args["csrf_token"])
    unread = messages.check_unread(user_id)
    username = request.args["user"].lower()
    title = request.args["title"].lower()
    description = request.args["description"].lower()
    price_low = request.args["price_low"]
    price_high = request.args["price_high"]
    results = ads.search(username, title, description, price_low, price_high)
    return render_template("ads.html", all_ads=results, unread=unread)

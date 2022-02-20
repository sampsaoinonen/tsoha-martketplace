from flask import flash

def register(username, password1, password2):
    if len(username) < 3 or len(username) > 20:
        flash("Username has to be between 3 and 20 characters!")
        return False
    if len(password1) < 5 or len(password1) > 20:
        flash("Password has to be between 5 and 20 characters!")
        return False
    if password1 != password2:
        flash("Passwords don't mach!")
        return False
    return True

def new_ad(title, description, phone, email, location, price, expires):
    if len(title) < 3 or len(title) > 30:
        flash("Title has to be between 3 and 30 characters!")
        return False
    if len(description) < 3 or len(description) > 200:
        flash("Description has to be between 3 and 200 characters!")
        return False
    if len(phone) > 20:
        flash("Phone number has to be at most 20 characters!")
        return False
    if len(email) > 50:
        flash("Email address has to be at most 20 characters!")
        return False
    if len(location) > 50:
        flash("Location has to be at most 50 characters!")
        return False    
    if int(price) < 0 or int(price) > 9999999.99:
        flash("Price has to be between 0 and 9,999,999.99")
        return False    
    if int(expires) < 1 or int(expires) > 365:
        flash("Number of days have to be between 1 and 365!")
        return False
    return True

def new_message(subject, message):
    if len(subject) < 3 or len(subject) > 30:
        flash("Subject has to be between 3 and 30 characters!")
        return False
    if len(message) < 3 or len(message) > 200:
        flash("Message has to be between 3 and 200 characters!")
        return False
    return True

def search(username, title, description, price_low, price_high):
    if len(username) > 20:
        flash("Username has to be no more than 20 characters!")
        return False
    if len(title) > 30:
        flash("Title has to be no more than 30 characters!")
        return False
    if len(description) > 30:
        flash("Description has to be no more than 30 characters!")
        return False
    if int(price_low) < 0 or int(price_low) > 9999999.99:
        flash("Price_low has to be between 0 and 9,999,999.99")
        return False
    if int(price_high) < 0 or int(price_high) > 10000000:
        flash("Price_low has to be between 0 and 9,999,999.99")
        return False
    return True

def image(file):
    extensions = [".jpg", "jpeg", "gif", "png"]
    if not file.filename.lower().endswith(tuple(extensions)):
        flash("Invalid filetype!")
        return False
    data = file.read()
    if len(data) > 1000*1024:
        flash("Your image is too big!")
        return False
    return True

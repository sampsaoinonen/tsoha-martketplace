from flask import flash

def register(username, password1, password2):
    if not (3 <= len(username) <= 20):
        flash("Username has to be between 3 and 20 characters!", "error")
        return False
    if not (5 <= len(password1) <= 20):
        flash("Password has to be between 5 and 20 characters!", "error")
        return False
    if password1 != password2:
        flash("Passwords don't match!", "error")
        return False
    return True

def new_ad(title, description, phone, email, location, price, expires, cat_id, type_id):
    if not (3 <= len(title) <= 30):
        flash("Title has to be between 3 and 30 characters!", "error")
        return False
    if not (3 <= len(description) <= 500):
        flash("Description has to be between 3 and 500 characters!", "error")
        return False
    if len(phone) > 20:
        flash("Phone number has to be at most 20 characters!", "error")
        return False
    if len(email) > 30:
        flash("Email address has to be at most 30 characters!", "error")
        return False
    if len(location) > 50:
        flash("Location has to be at most 50 characters!", "error")
        return False    
    if not (0 <= float(price) <= 9999999.99):
        flash("Price has to be between 0 and 9,999,999.99", "error")
        return False    
    if not (1 <= int(expires) <= 365):
        flash("Number of days have to be between 1 and 365!", "error")
        return False
    if cat_id == "Pick category - REQUIRED":
        flash("You have to select the category to continue!", "error")
        return False
    if type_id == "Pick type - REQUIRED":
        flash("You have to select the type to continue!", "error")
        return False
    return True

def new_message(subject, message):
    if not (3 <= len(subject) <= 30):
        flash("Subject has to be between 3 and 30 characters!", "error")
        return False
    if not (3 <= len(message) <= 500):
        flash("Message has to be between 3 and 500 characters!", "error")
        return False
    return True

def search(username, title, description, price_low, price_high):
    if len(username) > 20:
        flash("Username has to be no more than 20 characters!", "error")
        return False
    if len(title) > 30:
        flash("Title has to be no more than 30 characters!", "error")
        return False
    if len(description) > 30:
        flash("Description has to be no more than 30 characters!", "error")
        return False
    if not (0 <= int(price_low) <= 9999999.99):
        flash("Price Low has to be between 0 and 9,999,999.99", "error")
        return False
    if not (0 <= int(price_high) <= 10000000):
        flash("Price High has to be between 0 and 10,000,000", "error")
        return False
    return True

def search_profile(username):
    if len(username) > 20:
        flash("Username has to be no more than 20 characters!", "error")
        return False    
    return True

def image(image_name, data_size):         
    if not image_type(image_name):
        flash("Invalid filetype!", "error")
        return False         
    if data_size > 1000 * 1024:
        flash("Your image is too big!", "error")
        return False    
    return True

def image_type(filename):
    extensions = [".jpg", ".jpeg", ".gif", ".png"]
    return filename.lower().endswith(tuple(extensions)) 

def add_comment(content):
    if not (1 <= len(content) <= 500):
        flash("Comment has to be between 1 and 500 characters!", "error")
        return False
    return True

def update_description(description):
    if len(description) > 500:
        flash("Description has to be at most 500 characters!", "error")
        return False
    return True

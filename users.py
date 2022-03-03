from db import db
from flask import session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False    
    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["csrf_token"] = token_hex(16)
        return True    
    return False

def logout():
    del session["user_id"]
    del session["csrf_token"]

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id",0)

def check_csrf(form_token):
    if session["csrf_token"] != form_token:
        abort(403)

def search(username):    
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    message_id = result.fetchone()
    if not message_id:
        return False
    return message_id[0]

def get_profile(id):
    sql = "SELECT U.id, U.username, U.description, A.id, A.title FROM users U, ads A WHERE U.id=:id AND U.id=A.user_id"
    result = db.session.execute(sql, {"id":id})
    user_info = result.fetchall()
    if not user_info:
        return False
    return user_info

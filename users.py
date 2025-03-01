from db import db
from flask import session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex
from sqlalchemy.sql import text

def login(username, password):
    sql = text("SELECT id, password, admin FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False    
    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["admin"] = user.admin
        session["csrf_token"] = token_hex(16)
        return True    
    return False

def logout():
    session.pop("user_id", None)
    session.pop("admin", None)
    session.pop("csrf_token", None)

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username,password) VALUES (:username,:password)")
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id", 0)

def check_csrf(form_token):
    if session.get("csrf_token") != form_token:
        abort(403)

def search(username):    
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user_id = result.fetchone()
    return user_id[0] if user_id else False

def get_profile(id):
    sql = text("SELECT U.id, U.username, U.description, A.id, A.title, U.admin FROM users U LEFT JOIN ads A ON U.id=A.user_id WHERE U.id=:id")
    result = db.session.execute(sql, {"id": id})
    return result.fetchall()    

def search_profile(username, admin):
    sql = text("""SELECT id, username, description, admin FROM users 
                  WHERE LOWER(username) LIKE :username 
                  AND CAST(admin AS TEXT) LIKE :admin 
                  ORDER BY id""")    
    result = db.session.execute(sql, {"username": f"%{username}%", "admin": f"%{admin}%"})    
    return result.fetchall()

def update_description(description, user_id, profile_id):
    if user_id == profile_id or session.get("admin"):    
        sql = text("UPDATE users SET description=:description WHERE id=:profile_id")
        db.session.execute(sql, {"description": description, "profile_id": profile_id})
        db.session.commit()

def delete_user(user_id, profile_id):
    if user_id == profile_id or session.get("admin"):
        sql = text("DELETE FROM users WHERE id=:profile_id")
        db.session.execute(sql, {"profile_id": profile_id})
        db.session.commit()

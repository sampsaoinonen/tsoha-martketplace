from flask import session, make_response
from db import db

def add_ad_image(image_name, ad_id, data):       
    sql = "INSERT INTO ad_images (image_name, ad_id, data) VALUES (:image_name, :ad_id, :data)"
    db.session.execute(sql, {"image_name":image_name,"ad_id":ad_id, "data":data})    
    db.session.commit()

def add_user_image(image_name, user_id, data):  
    sql = "INSERT INTO user_images (image_name, user_id, data) VALUES (:image_name, :user_id, :data)"
    db.session.execute(sql, {"image_name":image_name,"user_id":user_id, "data":data})    
    db.session.commit()

def delete_ad_image(ad_id):
    db.session.execute("DELETE FROM ad_images WHERE ad_id=:ad_id",{"ad_id":ad_id})
    db.session.commit()

def delete_user_image(user_id):
    db.session.execute("DELETE FROM user_images WHERE user_id=:user_id",{"user_id":user_id})
    db.session.commit()

def get_ad_image(ad_id):
    sql = "SELECT data FROM ad_images WHERE ad_id=:ad_id"
    result = db.session.execute(sql, {"ad_id":ad_id})
    data = result.fetchone()[0]
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/jpeg")
    return response

def get_user_image(user_id):
    sql = "SELECT data FROM user_images WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    data = result.fetchone()[0]
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/jpeg")
    return response

def check_ad_image(ad_id):
    try:
        sql = "SELECT id FROM ad_images WHERE ad_id=:ad_id"
        result = db.session.execute(sql, {"ad_id":ad_id})
        return result.fetchone()[0]
    except:
        return False

def check_user_image(user_id):
    try:
        sql = "SELECT id FROM user_images WHERE user_id=:user_id"
        result = db.session.execute(sql, {"user_id":user_id})
        return result.fetchone()[0]
    except:
        return False
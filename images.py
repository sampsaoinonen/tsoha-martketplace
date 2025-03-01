from flask import session, make_response
from db import db
from sqlalchemy.sql import text

def add_ad_image(image_name, ad_id, data):       
    sql = text("INSERT INTO ad_images (image_name, ad_id, data) VALUES (:image_name, :ad_id, :data)")
    db.session.execute(sql, {"image_name": image_name, "ad_id": ad_id, "data": data})    
    db.session.commit()

def add_user_image(image_name, user_id, data):  
    sql = text("INSERT INTO user_images (image_name, user_id, data) VALUES (:image_name, :user_id, :data)")
    db.session.execute(sql, {"image_name": image_name, "user_id": user_id, "data": data})    
    db.session.commit()

def delete_ad_image(ad_id):
    db.session.execute(text("DELETE FROM ad_images WHERE ad_id=:ad_id"), {"ad_id": ad_id})
    db.session.commit()

def delete_user_image(user_id):
    db.session.execute(text("DELETE FROM user_images WHERE user_id=:user_id"), {"user_id": user_id})
    db.session.commit()

def get_ad_image(ad_id):
    sql = text("SELECT data FROM ad_images WHERE ad_id=:ad_id")
    result = db.session.execute(sql, {"ad_id": ad_id}).fetchone()
    if result:
        data = result[0]
        response = make_response(bytes(data))
        response.headers.set("Content-Type", "image/jpeg")
        return response
    return None

def get_user_image(user_id):
    sql = text("SELECT data FROM user_images WHERE user_id=:user_id")
    result = db.session.execute(sql, {"user_id": user_id}).fetchone()
    if result:
        data = result[0]
        response = make_response(bytes(data))
        response.headers.set("Content-Type", "image/jpeg")
        return response
    return None

def check_ad_image(ad_id):
    sql = text("SELECT id FROM ad_images WHERE ad_id=:ad_id")
    result = db.session.execute(sql, {"ad_id": ad_id}).fetchone()
    return result[0] if result else False

def check_user_image(user_id):
    sql = text("SELECT id FROM user_images WHERE user_id=:user_id")
    result = db.session.execute(sql, {"user_id": user_id}).fetchone()
    return result[0] if result else False

from flask import session, make_response
from db import db

def add_adimage(image_name, ad_id, data):       
    sql = '''INSERT INTO adimages (image_name, ad_id, data) VALUES (:image_name, :ad_id, :data)'''
    result = db.session.execute(sql, {"image_name":image_name,"ad_id":ad_id, "data":data})    
    db.session.commit()

def add_userimage(image_name, user_id, data):  
    sql = '''INSERT INTO userimages (image_name, user_id, data) VALUES (:image_name, :user_id, :data)'''
    result = db.session.execute(sql, {"image_name":image_name,"user_id":user_id, "data":data})    
    db.session.commit()

def get_adimage(ad_id):
    sql = "SELECT data FROM adimages WHERE ad_id=:ad_id"
    result = db.session.execute(sql, {"ad_id":ad_id})
    data = result.fetchone()[0]
    response = make_response(bytes(data))
    response.headers.set('Content-Type', 'image/jpeg')
    return response

def get_userimage(user_id):
    sql = "SELECT data FROM userimages WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    data = result.fetchone()[0]
    response = make_response(bytes(data))
    response.headers.set('Content-Type', 'image/jpeg')
    return response

def check_adimage(ad_id):
    try:
        sql = "SELECT id FROM adimages WHERE ad_id=:ad_id"
        result = db.session.execute(sql, {"ad_id":ad_id})
        return result.fetchone()[0]
    except:
        return False

def check_userimage(user_id):
    try:
        sql = "SELECT id FROM userimages WHERE user_id=:user_id"
        result = db.session.execute(sql, {"user_id":user_id})
        return result.fetchone()[0]
    except:
        return False
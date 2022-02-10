from flask import session
from db import db

def add_adimage(image_name, ad_id, data):       
    sql = '''INSERT INTO adimages (image_name, ad_id, data) VALUES (:image_name, :ad_id, 
    :data)'''
    result = db.session.execute(sql, {"image_name":image_name,"ad_id":ad_id, "data":data})    
    db.session.commit()

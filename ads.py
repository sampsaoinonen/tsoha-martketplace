from db import db

def get_ads():
    sql = '''SELECT A.id, A.title, A.description, A.phone, A.email, A.location, A.price, A.sent_at, U.username, C.cat_name FROM ads A, categories C, users U
    WHERE C.id=A.cat_id AND U.id=A.user_id
    GROUP BY A.id, C.cat_name, U.username
    ORDER BY A.sent_at'''
    result = db.session.execute(sql)
    return result.fetchall()

def add_ad(title, description, phone, email, location, price, user_id, cat_id):    
    sql = '''INSERT INTO ads (title, description, phone, email, location, price, sent_at, user_id, cat_id)
    VALUES (:title, :description, :phone, :email, :location, :price, NOW(), :user_id, :cat_id)'''
    result = db.session.execute(sql, {"title":title,"description":description, "phone":phone,
    'email':email,'location':location,'price':price, 'user_id':user_id, 'cat_id':cat_id})
    db.session.commit()

def get_cats():
    result = db.session.execute("SELECT * FROM categories")
    return result.fetchall()
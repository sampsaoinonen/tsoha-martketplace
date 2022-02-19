from db import db

def get_ads():
    sql = '''SELECT A.id, A.title, A.description, A.phone, A.email, A.location, A.price, A.expires, A.sent_at, 
    U.username, C.cat_name, T.type_name FROM ads A, categories C, users U, adtypes T WHERE C.id=A.cat_id AND U.id=A.user_id
    AND T.id=A.type_id AND A.sent_at > current_date - A.expires GROUP BY A.id, C.id, U.id, T.id 
    ORDER BY A.sent_at DESC'''
    result = db.session.execute(sql)
    return result.fetchall()

def get_ad(ad_id):
    sql = '''SELECT A.id, A.title, A.description, A.phone, A.email, A.location, A.price, A.expires, A.sent_at, 
    U.username, C.cat_name FROM ads A, categories C, users U, adtypes T WHERE A.id=:ad_id AND C.id=A.cat_id
    AND U.id=A.user_id AND T.id=A.type_id'''
    result = db.session.execute(sql, {"ad_id":ad_id})
    return result.fetchone()

def add_ad(title, description, phone, email, location, price, expires, user_id, cat_id, type_id):    
    sql = '''INSERT INTO ads (title, description, phone, email, location, price, expires, sent_at, user_id, cat_id, 
    type_id) VALUES (:title, :description, :phone, :email, :location, :price, :expires, NOW(), :user_id, :cat_id, 
    :type_id) RETURNING id'''
    result = db.session.execute(sql, {"title":title,"description":description, "phone":phone, "email":email,
    "location":location,"price":price, "expires":expires, "user_id":user_id, "cat_id":cat_id, "type_id":type_id})
    db.session.commit()
    return result.fetchone()[0]

def get_cats():
    result = db.session.execute("SELECT id, cat_name FROM categories")
    return result.fetchall()

def get_types():
    result = db.session.execute("SELECT id, type_name FROM adtypes")
    return result.fetchall()

def search(username, title, description, price_low, price_high):
    sql = '''SELECT A.id, A.title, A.description, A.phone, A.email, A.location, A.price, A.expires, A.sent_at, 
    U.username, C.cat_name, T.type_name FROM ads A, categories C, users U, adtypes T WHERE C.id=A.cat_id AND U.id=A.user_id 
    AND T.id=A.type_id AND LOWER(U.username) LIKE :username AND LOWER(A.title) LIKE :title AND LOWER(A.description) 
    LIKE :description AND A.price >= :price_low AND A.price <= :price_high AND A.sent_at > current_date - A.expires 
    GROUP BY A.id, C.id, U.id, T.id ORDER BY A.sent_at DESC'''
    result = db.session.execute(sql, {"username":"%"+username+"%","title":"%"+title+"%", "description":"%"+description+"%",
    "price_low":price_low, "price_high":price_high})    
    return result.fetchall()

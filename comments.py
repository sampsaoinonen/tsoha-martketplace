from flask import session
from db import db

def get_ad_comments(ad_id):
    sql = """SELECT U.username, C.content, C.sent_at, C.id, U.id FROM ad_comments C, users U WHERE C.ad_id=:ad_id AND C.user_id=U.id
    ORDER BY C.sent_at"""
    result = db.session.execute(sql, {"ad_id":ad_id})
    return result.fetchall()

def add_ad_comment(content, ad_id, user_id):
    sql = "INSERT INTO ad_comments (content, sent_at, ad_id, user_id) VALUES (:content, NOW(), :ad_id, :user_id)"
    db.session.execute(sql, {"content":content, "ad_id":ad_id, "user_id":user_id})
    db.session.commit()

def delete_ad_comment(user_id, ad_comment_id):    
    if session["admin"]:        
        db.session.execute("DELETE FROM ad_comments WHERE id=:ad_comment_id", {"ad_comment_id":ad_comment_id})
        db.session.commit()
    else:
        db.session.execute("DELETE FROM ad_comments WHERE id=:ad_comment_id AND user_id=:user_id",{"user_id":user_id, "ad_comment_id":ad_comment_id})
        db.session.commit()    

def check_ad_comment(ad_comment_id):
    result = db.session.execute("SELECT id FROM ad_comments WHERE id=:ad_comment_id", {"ad_comment_id":ad_comment_id})
    return result.fetchone()

def get_user_comments(profile_id):
    sql = """SELECT U.username, C.content, C.sent_at, C.id, U.id FROM user_comments C, users U WHERE C.profile_id=:profile_id AND C.commentator_id=U.id
    ORDER BY C.sent_at"""
    result = db.session.execute(sql, {"profile_id":profile_id})
    return result.fetchall()

def add_user_comment(content, commentator_id, profile_id):
    sql = "INSERT INTO user_comments (content, sent_at, commentator_id, profile_id) VALUES (:content, NOW(), :commentator_id, :profile_id)"
    db.session.execute(sql, {"content":content, "commentator_id":commentator_id, "profile_id":profile_id})
    db.session.commit()

def delete_user_comment(user_id, user_comment_id):    
    if session["admin"]:        
        result = db.session.execute("DELETE FROM user_comments WHERE id=:user_comment_id", {"user_comment_id":user_comment_id})
        db.session.commit()
    else:
        result = db.session.execute("DELETE FROM user_comments WHERE id=:user_comment_id AND commentator_id=:user_id",
        {"user_id":user_id, "user_comment_id":user_comment_id})
        db.session.commit()    

def check_user_comment(user_comment_id):
    result = db.session.execute("SELECT id FROM user_comments WHERE id=:user_comment_id", {"user_comment_id":user_comment_id})
    return result.fetchone()

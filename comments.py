from db import db

def get_ad_comments(ad_id):
    sql = """SELECT U.username, C.content, C.sent_at FROM ad_comments C, users U WHERE C.ad_id=:ad_id AND C.user_id=U.id
    ORDER BY C.sent_at"""
    result = db.session.execute(sql, {"ad_id":ad_id})
    return result.fetchall()

def add_ad_comment(content, ad_id, user_id):
    sql = "INSERT INTO ad_comments (content, sent_at, ad_id, user_id) VALUES (:content, NOW(), :ad_id, :user_id)"
    db.session.execute(sql, {"content":content, "ad_id":ad_id, "user_id":user_id})
    db.session.commit()

def get_user_comments(profile_id):
    sql = """SELECT U.username, C.content, C.sent_at FROM user_comments C, users U WHERE C.profile_id=:profile_id AND C.commentator_id=U.id
    ORDER BY C.sent_at"""
    result = db.session.execute(sql, {"profile_id":profile_id})
    return result.fetchall()

def add_user_comment(content, commentator_id, profile_id):
    sql = "INSERT INTO user_comments (content, sent_at, commentator_id, profile_id) VALUES (:content, NOW(), :commentator_id, :profile_id)"
    db.session.execute(sql, {"content":content, "commentator_id":commentator_id, "profile_id":profile_id})
    db.session.commit()
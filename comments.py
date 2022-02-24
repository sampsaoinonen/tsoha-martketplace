from db import db

def get_adcomments(ad_id):
    sql = '''SELECT U.username, C.content, C.sent_at FROM adcomments C, users U WHERE C.ad_id=:ad_id AND C.user_id=U.id
    ORDER BY C.sent_at DESC'''
    result = db.session.execute(sql, {"ad_id":ad_id})
    return result.fetchall()

def add_adcomment(content, ad_id, user_id):
    sql = "INSERT INTO adcomments (content, sent_at, ad_id, user_id) VALUES (:content, NOW(), :ad_id, :user_id)"
    db.session.execute(sql, {"content":content, "ad_id":ad_id, "user_id":user_id})
    db.session.commit()
from db import db

def send(user_from, user_to, subject, message):
    sql = '''INSERT INTO messages (user_from, user_to, subject, message, sent_at, seen) 
    VALUES (:user_from, :user_to, :subject, :message, NOW(), FALSE) RETURNING id'''
    result = db.session.execute(sql, {"user_from":user_from,"user_to":user_to, "subject":subject, "message":message})
    db.session.commit()    

def get_one(user_to, message_id):
    sql = '''SELECT M.id, M.user_from, M.user_to, M.subject, M.message, M.sent_at, M.seen, U.username 
    FROM messages M, users U WHERE M.id=:message_id AND U.id=M.user_from AND U.id=M.user_to
    AND M.user_to=:user_to'''
    result = db.session.execute(sql, {"user_to":user_to, "message_id":message_id})
    return result.fetchone()

def get_received(user_to):
    sql = '''SELECT M.id, M.user_from, M.user_to, M.subject, M.message, M.sent_at, M.seen, U.username
    FROM messages M, users U WHERE M.user_to=:user_to and U.id=M.user_from GROUP BY M.id, U.username
    ORDER BY sent_at DESC'''
    result = db.session.execute(sql, {"user_to":user_to})
    return result.fetchall()

def get_sent(user_from):
    sql = '''SELECT user_from, user_to, subject, message, sent_at, seen, username 
    FROM messages M, users U WHERE M.user_from=:user_from AND U.id=M.user_from AND U.id=M.user_to'''
    result = db.session.execute(sql, {"user_from":user_from})
    return result.fetchall()

#def read(message_id):
    
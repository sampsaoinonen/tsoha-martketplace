from db import db
from sqlalchemy.sql import text

def send(user_from, user_to, subject, message):
    sql = text("""INSERT INTO messages (user_from, user_to, subject, message, sent_at, seen) 
    VALUES (:user_from, :user_to, :subject, :message, NOW(), FALSE) RETURNING id""")
    result = db.session.execute(sql, {"user_from": user_from, "user_to": user_to, "subject": subject, "message": message})
    db.session.commit()
    return result.fetchone()[0]

def get_one_inbox(user_to, message_id):
    sql = text("""SELECT M.id, M.user_from, M.user_to, M.subject, M.message, M.sent_at, M.seen, U.username 
    FROM messages M LEFT JOIN users U ON U.id=M.user_from WHERE M.id=:message_id AND M.user_to=:user_to""")
    result = db.session.execute(sql, {"user_to": user_to, "message_id": message_id})
    return result.fetchone()

def get_one_sent(user_from, message_id):
    sql = text("""SELECT M.id, M.user_from, M.user_to, M.subject, M.message, M.sent_at, M.seen, U.username 
    FROM messages M LEFT JOIN users U ON U.id=M.user_to WHERE M.id=:message_id AND M.user_from=:user_from""")
    result = db.session.execute(sql, {"user_from": user_from, "message_id": message_id})
    return result.fetchone()

def get_inbox(user_to):
    sql = text("""SELECT M.id, M.user_from, M.user_to, M.subject, M.message, M.sent_at, M.seen, U.username
    FROM messages M LEFT JOIN users U ON U.id=M.user_from WHERE M.user_to=:user_to ORDER BY sent_at DESC""")
    result = db.session.execute(sql, {"user_to": user_to})
    return result.fetchall()

def get_sent(user_from):
    sql = text("""SELECT M.id, M.user_from, M.user_to, M.subject, M.message, M.sent_at, M.seen, U.username
    FROM messages M LEFT JOIN users U ON U.id=M.user_to WHERE M.user_from=:user_from ORDER BY sent_at DESC""")
    result = db.session.execute(sql, {"user_from": user_from})
    return result.fetchall()

def seen(message_id):
    sql = text("UPDATE messages SET seen=TRUE WHERE id=:message_id")
    db.session.execute(sql, {"message_id": message_id})
    db.session.commit()

def check_unread(user_to):
    sql = text("SELECT COUNT(id) FROM messages WHERE user_to=:user_to AND seen=FALSE")
    result = db.session.execute(sql, {"user_to": user_to})
    return result.fetchone()

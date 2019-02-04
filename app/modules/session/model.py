from datetime import datetime
from db import DB

def sessionExist(session_id):
    db = DB()
    query = """
        SELECT `visits`
        FROM `{table}`
        WHERE `id` = %s
    """.format(table=db.table('sessions'))
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, [session_id])
    connection.close()
    data = cursor.fetchone()
    return data and 'visits' in data

def createSession(session_id):
    db = DB()
    query = """
        INSERT INTO `{table}` (`id`, `start`)
        VALUES (%s, %s)
    """.format(table=db.table('sessions'))
    connection = db.getConnection()
    cursor = connection.cursor()
    start = datetime.now()
    cursor.execute(query, [session_id, start])
    connection.commit()
    connection.close()

def increaseVisits(session_id):
    db = DB()
    query = """
        UPDATE `{table}`
        SET `visits` = `visits` + 1
        WHERE `id` = %s
    """.format(table=db.table('sessions'))
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, [session_id])
    connection.commit()
    connection.close()
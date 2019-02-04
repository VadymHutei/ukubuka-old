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
        INSERT INTO `{table}` (`id`, `start`, `last_visit`)
        VALUES (%s, %s, %s)
    """.format(table=db.table('sessions'))
    connection = db.getConnection()
    cursor = connection.cursor()
    start = datetime.now()
    cursor.execute(query, [session_id, start, start])
    connection.commit()
    connection.close()

def increaseVisits(session_id, remote_address=None):
    db = DB()
    query = """
        UPDATE `{table}`
        SET
            `visits` = `visits` + 1,
            `remote_address` = %s,
            `last_visit` = %s
        WHERE `id` = %s
    """.format(table=db.table('sessions'))
    current_datetime = datetime.now()
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, [remote_address, current_datetime, session_id])
    connection.commit()
    connection.close()
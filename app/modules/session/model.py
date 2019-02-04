from datetime import datetime
from db import DB

def is_available(session_id):
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
    if data: return 'visits' not in data
    return True

def create_session(session_id):
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
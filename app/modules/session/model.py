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

def getUserIdByEmail(email):
    db = DB()
    query = """
        SELECT `user_id`
        FROM `{table}`
        WHERE `property` = 'email'
        AND `value` = %s
    """.format(table=db.table('users_data'))
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, [email])
    connection.close()
    data = cursor.fetchone()
    return data['user_id'] if data and 'user_id' in data else False

def getUserIdByUIC(uic):
    db = DB()
    query = """
        SELECT `user_id`
        FROM `{table}`
        WHERE `token` = %s
    """.format(table=db.table('tokens'))
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, [uic])
    connection.close()
    data = cursor.fetchone()
    return data['user_id'] if data and 'user_id' in data else False

def getUserAuthenticationData(user_id):
    result = {}
    properties = ('salt', 'password')
    db = DB()
    query = """
        SELECT `property`, `value`
        FROM `{table}`
        WHERE `user_id` = %s
        AND `property` IN ({properties})
    """.format(
        table=db.table('users_data'),
        properties = ', '.join(["'" + prop + "'" for prop in properties])
    )
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, [user_id])
    connection.close()
    data = cursor.fetchall()
    for row in data:
        if row['property'] in properties: result[row['property']] = row['value']
    return result if len(result) == len(properties) else False

def setUIC(uic, user_id, start, expired):
    db = DB()
    query = """
        INSERT INTO `{table}` (`token`, `user_id`, `start`, `expired`)
        VALUES (%s, %s, %s, %s)
    """.format(table=db.table('tokens'))
    connection = db.getConnection()
    cursor = connection.cursor()
    start = datetime.now()
    cursor.execute(query, [uic, user_id, start, expired])
    connection.commit()
    connection.close()

def getUICExpired(uic):
    db = DB()
    query = """
        SELECT `expired`
        FROM `{table}`
        WHERE `token` = %s
    """.format(table=db.table('tokens'))
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, [uic])
    connection.close()
    data = cursor.fetchone()
    return data['expired'] if 'expired' in data else False

def getUserGroup(user_id):
    result = {}
    db = DB()
    query = """
        SELECT g.`name` `group`
        FROM `{table_u}` u
        LEFT JOIN {table_g} g
            ON u.`group_id` = g.`id`
        WHERE u.`id` = %s
    """.format(
        table_u=db.table('users'),
        table_g=db.table('users_groups')
    )
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, [user_id])
    connection.close()
    data = cursor.fetchone()
    return data['group'] if 'group' in data else False
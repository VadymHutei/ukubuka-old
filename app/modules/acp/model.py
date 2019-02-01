from db import DB



#     ##     ## ######## ##    ## ##     ##  ######
#     ###   ### ##       ###   ## ##     ## ##    ##
#     #### #### ##       ####  ## ##     ## ##
#     ## ### ## ######   ## ## ## ##     ##  ######
#     ##     ## ##       ##  #### ##     ##       ##
#     ##     ## ##       ##   ### ##     ## ##    ##
#     ##     ## ######## ##    ##  #######   ######



def getMenus(lang):
    db = DB()
    query = """
        SELECT
            m.`id`,
            m.`menu`,
            m.`parent`,
            m.`is_active`,
            m.`link`,
            t.`name`
        FROM `{table}` m
        LEFT JOIN `{table}_text` t
            ON m.`id` = t.`item_id`
        AND `language` = '{lang}'
    """.format(table=db.table('menus'), lang=lang)
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query)
    connection.close()
    menus_items = cursor.fetchall()
    layers = []
    layer = []
    result = {}
    temp = {}
    for item in menus_items:
        if item['parent'] is None:
            layer.append(item['id'])
        temp[item['id']] = item
    layer_count = len(layer)
    if layer_count:
        layers.append(layer)
        while layer_count > 0:
            layer_count = 0
            layer = []
            for item in menus_items:
                if item['parent'] in layers[-1]:
                    layer.append(item['id'])
            layer_count = len(layer)
            if layer_count:
                layers.append(layer)
    while layers:
        for item_id in layers.pop():
            if temp[item_id]['parent'] is not None:
                if 'submenu' not in temp[temp[item_id]['parent']]: temp[temp[item_id]['parent']]['submenu'] = []
                temp[temp[item_id]['parent']]['submenu'].append(temp.pop(item_id))
            else:
                temp[item_id]['parent'] = '-'
    for item_id in temp:
        if temp[item_id]['menu'] not in result: result[temp[item_id]['menu']] = []
        result[temp[item_id]['menu']].append(temp[item_id])
    return result

def getMenuItem(item_id):
    db = DB()
    query = """
        SELECT m.*, t.`language`, t.`name`
        FROM `{table}` m
        INNER JOIN `{table}_text` t
            ON m.`id` = t.`item_id`
        WHERE m.`id` = %s
    """.format(table=db.table('menus'))
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, [item_id])
    connection.close()
    item_data = cursor.fetchall()
    result = {}
    for row in item_data:
        if not result:
            for field in row:
                if field == 'name':
                    result['name'] = {row['language']: row['name']}
                else:
                    result[field] = row[field]
        else:
            result['name'][row['language']] = row['name']
    return result

def addMenuItem(data):
    columns = ['menu', 'is_active']
    values = [data['menu'], data['is_active']]
    placeholders = ['%s', '%s']
    if 'parent' in data:
        columns.append('parent')
        values.append(data['parent'])
        placeholders.append('%s')
    if 'link' in data:
        columns.append('link')
        values.append(data['link'])
        placeholders.append('%s')
    db = DB()
    query = """
        INSERT INTO `{table}` ({columns})
        VALUES ({placeholders})
    """.format(
        table=db.table('menus'),
        columns=', '.join(map(lambda x: '`' + x + '`', columns)),
        placeholders=', '.join(placeholders)
    )
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, values)
    values = [
        [cursor.lastrowid, 'ukr', data['name_ukr']],
        [cursor.lastrowid, 'eng', data['name_eng']]
    ]
    query = """
        INSERT INTO `{table}` (`item_id`, `language`, `name`)
        VALUES (%s, %s, %s)
    """.format(table=db.table('menus_text'))
    cursor.executemany(query, values)
    connection.commit()
    connection.close()

def editMenuItem(data):
    columns = [
        'menu',
        'is_active',
        'parent',
        'link'
    ]
    values = [
        data['menu'],
        data['is_active']
    ]
    values.append(data['parent'] if 'parent' in data else None)
    values.append(data['link'] if 'link' in data else None)
    columns = ','.join(['`{column}` = %s'.format(column=column) for column in columns]) if columns else ''
    values.append(data['item_id'])
    db = DB()
    query = """
        UPDATE `{table}`
        SET {additional_columns}
        WHERE `id` = %s
    """.format(
        table=db.table('menus'),
        additional_columns=columns
    )
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, values)
    columns = ['item_id', 'language', 'name']
    values = [
        [data['name_ukr'], data['item_id'], 'ukr'],
        [data['name_eng'], data['item_id'], 'eng']
    ]
    query = """
        UPDATE `{table}`
        SET `name` = %s
        WHERE `item_id` = %s
        AND `language` = %s
    """.format(
        table=db.table('menus_text'),
        additional_columns=columns
    )
    cursor.executemany(query, values)
    connection.commit()
    connection.close()

def deleteMenuItem(item_id):
    db = DB()
    query = """
        DELETE FROM `{table}`
        WHERE `id` = %s
    """.format(table=db.table('menus'))
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, [item_id])
    connection.commit()
    connection.close()



#     ##     ##  ######  ######## ########   ######
#     ##     ## ##    ## ##       ##     ## ##    ##
#     ##     ## ##       ##       ##     ## ##
#     ##     ##  ######  ######   ########   ######
#     ##     ##       ## ##       ##   ##         ##
#     ##     ## ##    ## ##       ##    ##  ##    ##
#      #######   ######  ######## ##     ##  ######



user_properties = ('first_name', 'patronymic', 'last_name', 'phone_number', 'email')
user_multiproperties = {'phone_numbers': 'phone_number', 'emails': 'email'}

def getUsers():
    db = DB()
    query = """
        SELECT u.`id`, u.`group_id`, ug.`name` group_name, u.`is_active`
        FROM `{table_u}` u
        LEFT JOIN `{table_ug}` ug
            ON ug.`id` = u.`group_id`
    """.format(
        table_u=db.table('users'),
        table_ug=db.table('users_groups')
    )
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query)
    users = cursor.fetchall()
    if not users: return []
    users_ids = [str(user['id']) for user in users]
    query = """
        SELECT `user_id`, `property`, `value`
        FROM `{table}`
        WHERE `user_id` IN ({users_ids})
    """.format(
        table=db.table('users_data'),
        users_ids=', '.join(users_ids)
    )
    cursor.execute(query)
    users_data = cursor.fetchall()
    connection.close()
    users = {user['id']: user for user in users}
    multivalues = ('email', 'phone_number')
    for row in users_data:
        if row['user_id'] not in users: continue
        if row['property'] in multivalues:
            if row['property'] not in users[row['user_id']]: users[row['user_id']][row['property']] = []
            users[row['user_id']][row['property']].append(row['value'])
        else:
            users[row['user_id']][row['property']] = row['value']
    return users

def getUser(user_id):
    db = DB()
    query = """
        SELECT u.`id`, u.`group_id`, ug.`name` group_name, u.`is_active`
        FROM `{table_u}` u
        LEFT JOIN `{table_ug}` ug
            ON ug.`id` = u.`group_id`
        WHERE u.`id` = %s
    """.format(
        table_u=db.table('users'),
        table_ug=db.table('users_groups')
    )
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, [user_id])
    user = cursor.fetchone()
    query = """
        SELECT `user_id`, `property`, `value`
        FROM `{table}`
        WHERE `user_id` = %s
    """.format(table=db.table('users_data'))
    cursor.execute(query, [user_id])
    user_data = cursor.fetchall()
    connection.close()
    multivalues = ('email', 'phone_number')
    for row in user_data:
        if row['property'] in multivalues:
            if row['property'] not in user: user[row['property']] = []
            user[row['property']].append(row['value'])
        else:
            user[row['property']] = row['value']
    return user

def addUser(data):
    db = DB()
    values = [
        data['group_id'],
        data['is_active']
    ]
    query = """
        INSERT INTO `{table}` (`group_id`, `is_active`)
        VALUES (%s, %s)
    """.format(table=db.table('users'))
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, values)
    values = []
    for prop in data:
        if prop not in user_properties: continue
        values.append([cursor.lastrowid, prop, data[prop]])
    if values:
        query = """
            INSERT INTO `{table}` (`user_id`, `property`, `value`)
            VALUES (%s, %s, %s)
        """.format(table=db.table('users_data'))
        cursor.executemany(query, values)
    connection.commit()
    connection.close()

def editUser(data):
    db = DB()
    connection = db.getConnection()
    cursor = connection.cursor()
    if 'group_id' in data or 'is_active' in data:
        columns = []
        values = []
        if 'group_id' in data:
            columns.append('group_id')
            values.append(data['group_id'])
        if 'is_active' in data:
            columns.append('is_active')
            values.append(data['is_active'])
        values.append(data['user_id'])
        query = """
            UPDATE `{table}`
            SET {values}
            WHERE `id` = %s
        """.format(
            table=db.table('users'),
            values=', '.join('`{column}` = %s'.format(column=column) for column in columns)
        )
        cursor.execute(query, values)
        connection.commit()
    query = """
        DELETE FROM `{table}`
        WHERE `user_id` = %s
    """.format(table=db.table('users_data'))
    cursor.execute(query, [data['user_id']])
    values = []
    for prop in data:
        if prop in user_properties:
            values.append([data['user_id'], prop, data[prop]])
        if prop in user_multiproperties:
            for value in data[prop]:
                values.append([data['user_id'], user_multiproperties[prop], value])
    if values:
        query = """
            INSERT INTO `{table}` (`user_id`, `property`, `value`)
            VALUES (%s, %s, %s)
        """.format(table=db.table('users_data'))
        print(query)
        print(values)
        cursor.executemany(query, values)
        connection.commit()
    connection.close()

def deleteUser(user_id):
    db = DB()
    query = """
        DELETE FROM `{table}`
        WHERE `id` = %s
    """.format(table=db.table('users'))
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, [user_id])
    connection.commit()
    connection.close()



#     ##     ##  ######  ######## ########   ######      ######   ########   #######  ##     ## ########   ######
#     ##     ## ##    ## ##       ##     ## ##    ##    ##    ##  ##     ## ##     ## ##     ## ##     ## ##    ##
#     ##     ## ##       ##       ##     ## ##          ##        ##     ## ##     ## ##     ## ##     ## ##
#     ##     ##  ######  ######   ########   ######     ##   #### ########  ##     ## ##     ## ########   ######
#     ##     ##       ## ##       ##   ##         ##    ##    ##  ##   ##   ##     ## ##     ## ##              ##
#     ##     ## ##    ## ##       ##    ##  ##    ##    ##    ##  ##    ##  ##     ## ##     ## ##        ##    ##
#      #######   ######  ######## ##     ##  ######      ######   ##     ##  #######   #######  ##         ######



def getUsersGroups():
    db = DB()
    query = 'SELECT * FROM `{table}`'.format(table=db.table('users_groups'))
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query)
    connection.close()
    users_groups = cursor.fetchall()
    return users_groups

def getUsersGroup(group_id):
    db = DB()
    query = """
        SELECT `id`, `name`
        FROM `{table}`
        WHERE `id` = %s
    """.format(table=db.table('users_groups'))
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, [group_id])
    connection.close()
    group_data = cursor.fetchone()
    return group_data

def addUsersGroup(data):
    values = [data['name']]
    db = DB()
    query = """
        INSERT INTO `{table}` (`name`)
        VALUES (%s)
    """.format(table=db.table('users_groups'))
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    connection.close()

def editUsersGroup(data):
    values = [data['name'], data['group_id']]
    db = DB()
    query = """
        UPDATE `{table}`
        SET `name` = %s
        WHERE `id` = %s
    """.format(table=db.table('users_groups'))
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    connection.close()

def deleteUsersGroup(users_group_id):
    db = DB()
    query = """
        DELETE FROM `{table}`
        WHERE `id` = %s
    """.format(table=db.table('users_groups'))
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, [users_group_id])
    connection.commit()
    connection.close()
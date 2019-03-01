import config
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



#      ######     ###    ######## ########  ######    #######  ########  #### ########  ######
#     ##    ##   ## ##      ##    ##       ##    ##  ##     ## ##     ##  ##  ##       ##    ##
#     ##        ##   ##     ##    ##       ##        ##     ## ##     ##  ##  ##       ##
#     ##       ##     ##    ##    ######   ##   #### ##     ## ########   ##  ######    ######
#     ##       #########    ##    ##       ##    ##  ##     ## ##   ##    ##  ##             ##
#     ##    ## ##     ##    ##    ##       ##    ##  ##     ## ##    ##   ##  ##       ##    ##
#      ######  ##     ##    ##    ########  ######    #######  ##     ## #### ########  ######



def getCategory(category_id, language):
    db = DB()
    query = """
        SELECT
            c.`id`,
            c.`parent`, 
            t.`name` 
        FROM `{table}` c
        LEFT JOIN `{table_text}` t
            ON c.`id` = t.`category_id`
        WHERE t.`language` = %s
        AND c.`id` = %s
    """.format(
        table=db.table('categories'),
        table_text=db.table('categories_text')
    )
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, [language, category_id])
    connection.close()
    return cursor.fetchone()

def getCategories(language):
    db = DB()
    query = """
        SELECT
            c.`id`,
            c.`parent`, 
            t.`name` 
        FROM `{table}` c
        LEFT JOIN `{table_text}` t
            ON c.`id` = t.`category_id`
        WHERE t.`language` = %s
    """.format(
        table=db.table('categories'),
        table_text=db.table('categories_text')
    )
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, [language])
    data = cursor.fetchall()
    connection.close()
    if not data: return {}
    categories = {row['id']: row for row in data}
    for category_id in categories:
        if categories[category_id]['parent'] is not None:
            if categories[category_id]['parent'] in categories:
                categories[category_id]['parent'] = categories[categories[category_id]['parent']]
    return categories

def getSubcategories(parent, language):
    db = DB()
    categories_data = []
    parents = [parent]
    connection = db.getConnection()
    cursor = connection.cursor()
    while parents:
        query = """
            SELECT
                c.`id`,
                c.`parent`, 
                t.`name` 
            FROM `{table}` c
            LEFT JOIN `{table_text}` t
                ON c.`id` = t.`category_id`
            WHERE t.`language` = %s
            AND c.`parent` IN %s
        """.format(
            table=db.table('categories'),
            table_text=db.table('categories_text')
        )
        cursor.execute(query, [language, parents])
        data = cursor.fetchall()
        if data: categories_data += data
        parents = [x['id'] for x in data]
    connection.close()
    if not categories_data: return {}
    categories = {row['id']: row for row in categories_data}
    for category_id in categories:
        if categories[category_id]['parent'] is not None:
            if categories[category_id]['parent'] in categories:
                categories[category_id]['parent'] = categories[categories[category_id]['parent']]
    return categories



#     ##     ##  ######  ######## ########   ######
#     ##     ## ##    ## ##       ##     ## ##    ##
#     ##     ## ##       ##       ##     ## ##
#     ##     ##  ######  ######   ########   ######
#     ##     ##       ## ##       ##   ##         ##
#     ##     ## ##    ## ##       ##    ##  ##    ##
#      #######   ######  ######## ##     ##  ######



def getUsers():
    db = DB()
    query = """
        SELECT
            `id`,
            `group_id`,
            `first_name`,
            `last_name`,
            `patronymic`,
            `added`,
            `is_active`
        FROM `{table}`
    """.format(table=db.table('users'))
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query)
    users_data = cursor.fetchall()
    if not users_data:
        connection.close()
        return []
    user_ids = []
    users = {}
    for row in users_data:
        user_ids.append(row['id'])
        users[row['id']] = {
            'id': row['id'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'patronymic': row['patronymic'],
            'group_id': row['group_id'],
            'group': config.USERS_GROUPS.get(row['group_id'], ''),
            'added': row['added'].strftime('%d-%m-%Y %H:%M:%S'),
            'is_active': row['is_active'] == 'Y',
            'emails': [],
            'phone_numbers': []
        }
    query = """
        SELECT
            `user_id`,
            `email`
        FROM `{table}`
        WHERE `user_id` IN %s
    """.format(
        table=db.table('users_emails')
    )
    cursor.execute(query, [user_ids])
    user_emails_data = cursor.fetchall()
    query = """
        SELECT
            `user_id`,
            `phone_number`
        FROM `{table}`
        WHERE `user_id` IN %s
    """.format(
        table=db.table('users_phone_numbers')
    )
    cursor.execute(query, [user_ids])
    user_phone_numbers_data = cursor.fetchall()
    connection.close()
    for row in user_emails_data:
        if row['user_id'] in users:
            users[row['user_id']]['emails'].append(row['email'])
    for row in user_phone_numbers_data:
        if row['user_id'] in users:
            users[row['user_id']]['phone_numbers'].append(row['phone_number'])
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

def addUserPhoneNumber(data):
    db = DB()
    connection = db.getConnection()
    cursor = connection.cursor()
    values = [
        data['user_id'],
        'phone_number',
        data['phone_number']
    ]
    query = """
        INSERT INTO `{table}` (`user_id`, `property`, `value`)
        VALUES (%s, %s, %s)
    """.format(table=db.table('users_data'))
    cursor.execute(query, values)
    connection.commit()
    connection.close()

def addUserEmail(data):
    db = DB()
    connection = db.getConnection()
    cursor = connection.cursor()
    values = [
        data['user_id'],
        'email',
        data['email']
    ]
    query = """
        INSERT INTO `{table}` (`user_id`, `property`, `value`)
        VALUES (%s, %s, %s)
    """.format(table=db.table('users_data'))
    cursor.execute(query, values)
    connection.commit()
    connection.close()



#      ######  ######## ######## ######## #### ##    ##  ######    ######
#     ##    ## ##          ##       ##     ##  ###   ## ##    ##  ##    ##
#     ##       ##          ##       ##     ##  ####  ## ##        ##
#      ######  ######      ##       ##     ##  ## ## ## ##   ####  ######
#           ## ##          ##       ##     ##  ##  #### ##    ##        ##
#     ##    ## ##          ##       ##     ##  ##   ### ##    ##  ##    ##
#      ######  ########    ##       ##    #### ##    ##  ######    ######



def getSettings():
    db = DB()
    query = 'SELECT * FROM `{table}`'.format(table=db.table('settings'))
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query)
    connection.close()
    settings_data = cursor.fetchall()
    return {row['property']: row['value'] for row in settings_data}

def saveSettings(data):
    db = DB()
    query = """
        UPDATE `{table}`
        SET `value` = %s
        WHERE `property` = %s
    """.format(table=db.table('settings'))
    values = [[data[prop], prop] for prop in data]
    if values:
        connection = db.getConnection()
        cursor = connection.cursor()
        cursor.executemany(query, values)
        connection.commit()
        connection.close()
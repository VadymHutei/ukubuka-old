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



def getCategory(category_id):
    db = DB()
    query = """
        SELECT
            `id`,
            `parent`,
            `is_active`
        FROM `{table}`
        WHERE `id` = %s
    """.format(table=db.table('categories'))
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, (category_id))
    category_data = cursor.fetchone()
    if not category_data:
        connection.close()
        return {}
    query = """
        SELECT
            `language`,
            `name`
        FROM `{table}`
        WHERE `category_id` = %s
    """.format(table=db.table('categories_text'))
    cursor.execute(query, (category_id))
    connection.close()
    category_text_data = cursor.fetchall()
    for row in category_text_data:
        for prop in row:
            if prop == 'language': continue
            if prop not in category_data: category_data[prop] = {}
            category_data[prop][row['language']] = row[prop]
    return category_data

def getCategories(language, parent=None):
    result = {}
    db = DB()
    query = """
        SELECT
            c.`id`,
            c.`parent`,
            c.`added`,
            c.`is_active`,
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
    connection.close()
    categories_data = cursor.fetchall()
    if not categories_data: return result
    categories = {row['id']: row for row in categories_data}
    parents = {}
    for category_id in categories:
        if categories[category_id]['parent'] is None:
            result[category_id] = categories[category_id]
            result[category_id]['subcategories'] = {}
        else:
            if categories[category_id]['parent'] not in parents:
                parents[categories[category_id]['parent']] = []
            parents[categories[category_id]['parent']].append(category_id)
    def setSubcategories(result):
        for r_category_id in result:
            if r_category_id in parents:
                for p_category_id in parents[r_category_id]:
                    result[r_category_id]['subcategories'][p_category_id] = categories[p_category_id]
                    result[r_category_id]['subcategories'][p_category_id]['subcategories'] = {}
            if result[r_category_id]['subcategories']:
                setSubcategories(result[r_category_id]['subcategories'])
    setSubcategories(result)
    if parent is None:
        return result
    else:
        if type(parent) is str: parent = int(parent)
        def getSubcategories(parent, categories):
            for category_id in categories:
                if category_id == parent:
                    return categories[category_id]['subcategories']
                else:
                    subcategories = getSubcategories(parent, categories[category_id]['subcategories'])
                    if subcategories:
                        return subcategories
            return {}
        return getSubcategories(parent, result)

def getCategoriesNames(language):
    db = DB()
    query = """
        SELECT
            c.`id`,
            t.`name`
        FROM `{table}` c
        RIGHT JOIN `{table_text}` t
            ON c.`id` = t.`category_id`
        WHERE t.`language` = %s
    """.format(
        table=db.table('categories'),
        table_text=db.table('categories_text')
    )
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, (language,))
    connection.close()
    categories_names_data = cursor.fetchall()
    return {row['id']: row['name'] for row in categories_names_data} if categories_names_data else {}

def addCategory(data):
    db = DB()
    query = """
        INSERT INTO `{table}` (`parent`, `added`, `is_active`)
        VALUES (%s, %s, %s)
    """.format(table=db.table('categories'))
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, (data['parent'], data['added'], data['is_active']))
    category_id = cursor.lastrowid
    for language in config.LANGUAGES:
        prop = 'name_' + language
        if prop in data:
            query = """
                INSERT INTO `{table}` (`category_id`, `language`, `name`)
                VALUES (%s, %s, %s)
            """.format(table=db.table('categories_text'))
            cursor.execute(query, (category_id, language, data[prop]))
    connection.commit()
    connection.close()

def editCategory(data):
    db = DB()
    connection = db.getConnection()
    cursor = connection.cursor()
    categories_field = ('parent', 'is_active')
    columns = []
    values = []
    commit = False
    for prop in categories_field:
        if prop in data:
            columns.append(prop)
            values.append(data[prop])
    if columns:
        columns = ','.join(['`{column}` = %s'.format(column=column) for column in columns]) if columns else ''
        values.append(data['id'])
        query = """
            UPDATE `{table}`
            SET {additional_columns}
            WHERE `id` = %s
        """.format(
            table=db.table('categories'),
            additional_columns=columns
        )
        cursor.execute(query, values)
        commit = True
    if 'name_ukr' in data:
        query = """
            UPDATE `{table}`
            SET `name` = %s
            WHERE `category_id` = %s
            AND `language` = 'ukr'
        """.format(table=db.table('categories_text'))
        cursor.execute(query, (data['name_ukr'], data['id']))
        commit = True
    if 'name_eng' in data:
        query = """
            UPDATE `{table}`
            SET `name` = %s
            WHERE `category_id` = %s
            AND `language` = 'eng'
        """.format(table=db.table('categories_text'))
        cursor.execute(query, (data['name_eng'], data['id']))
        commit = True
    if commit: connection.commit()
    connection.close()

def deleteCategory(category_id):
    db = DB()
    query = """
        DELETE FROM `{table}`
        WHERE `id` = %s
    """.format(table=db.table('categories'))
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, [category_id])
    connection.commit()
    connection.close()



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
            'emails': [],
            'phone_numbers': [],
            'added': row['added'].strftime('%d-%m-%Y %H:%M:%S'),
            'is_active': row['is_active'] == 'Y'
        }
    query = """
        SELECT
            `user_id`,
            `email`
        FROM `{table}`
        WHERE `user_id` IN %s
    """.format(table=db.table('users_emails'))
    cursor.execute(query, [user_ids])
    user_emails_data = cursor.fetchall()
    query = """
        SELECT
            `user_id`,
            `phone_number`
        FROM `{table}`
        WHERE `user_id` IN %s
    """.format(table=db.table('users_phone_numbers'))
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
    connection = db.getConnection()
    cursor = connection.cursor()
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
        WHERE `id` = %s
    """.format(table=db.table('users'))
    cursor.execute(query, (user_id,))
    user_data = cursor.fetchone()
    if not user_data:
        connection.close()
        return False
    query = """
        SELECT `phone_number`
        FROM `{table}`
        WHERE `user_id` = %s
    """.format(table=db.table('users_phone_numbers'))
    cursor.execute(query, (user_id,))
    user_phone_numbers_data = cursor.fetchall()
    query = """
        SELECT `email`
        FROM `{table}`
        WHERE `user_id` = %s
    """.format(table=db.table('users_emails'))
    cursor.execute(query, (user_id,))
    user_emails_data = cursor.fetchall()
    connection.close()
    user = {}
    for prop in user_data:
        user[prop] = user_data[prop] if user_data[prop] is not None else ''
    if user_phone_numbers_data:
        user['phone_numbers'] = []
        for row in user_phone_numbers_data:
            user['phone_numbers'].append(row['phone_number'])
    if user_emails_data:
        user['emails'] = []
        for row in user_emails_data:
            user['emails'].append(row['email'])
    return user

def addUser(data):
    db = DB()
    users_fields = ('group_id', 'added', 'is_active', 'first_name', 'patronymic', 'last_name')
    fields = []
    values = []
    for field in users_fields:
        if field in data:
            values.append(data[field])
            fields.append('`' + field + '`')
    query = """
        INSERT INTO `{table}` ({fields})
        VALUES %s
    """.format(
        table=db.table('users'),
        fields=', '.join(fields)
    )
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, (values,))
    user_id = cursor.lastrowid
    if 'email' in data:
        query = """
            INSERT INTO `{table}` (`user_id`, `email`)
            VALUES (%s, %s)
        """.format(table=db.table('users_emails'))
        cursor.execute(query, [user_id, data['email']])
    if 'phone_number' in data:
        query = """
            INSERT INTO `{table}` (`user_id`, `phone_number`)
            VALUES (%s, %s)
        """.format(table=db.table('users_phone_numbers'))
        cursor.execute(query, [user_id, data['phone_number']])
    if 'salt' in data and 'password_hash' in data:
        query = """
            INSERT INTO `{table}` (`user_id`, `salt`, `password_hash`)
            VALUES (%s, %s, %s)
        """.format(table=db.table('users_passwords'))
        cursor.execute(query, [user_id, data['salt'], data['password_hash']])
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
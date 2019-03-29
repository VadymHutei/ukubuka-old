import config
from db import DB



#     ##     ## ######## ##    ## ##     ##  ######
#     ###   ### ##       ###   ## ##     ## ##    ##
#     #### #### ##       ####  ## ##     ## ##
#     ## ### ## ######   ## ## ## ##     ##  ######
#     ##     ## ##       ##  #### ##     ##       ##
#     ##     ## ##       ##   ### ##     ## ##    ##
#     ##     ## ######## ##    ##  #######   ######



def getMenuItem(item_id):
    db = DB()
    connection = db.getConnection()
    cursor = connection.cursor()
    query = """
        SELECT
            `id`,
            `parent`,
            `link`,
            `added`,
            `is_active`
        FROM `{table}`
        WHERE `id` = %s
    """.format(table=db.table('menus'))
    cursor.execute(query, (item_id,))
    item_data = cursor.fetchone()
    if not item_data:
        connection.close()
        return {}
    query = """
        SELECT
            `language`,
            `name`
        FROM `{table}`
        WHERE `item_id` = %s
    """.format(table=db.table('menus_text'))
    cursor.execute(query, (item_id,))
    connection.close()
    item_text_data = cursor.fetchall()
    item_data['name'] = {}
    for row in item_text_data:
        if 'language' not in row: continue
        if row['name'] is None: continue
        if row['language'] not in config.LANGUAGES: continue
        if row['language'] not in item_data['name']: item_data['name'][row['language']] = row['name']
    return item_data

def getMenus(lang, parent=None):
    result = {}
    db = DB()
    connection = db.getConnection()
    cursor = connection.cursor()
    query = """
        SELECT
            m.`id`,
            m.`parent`,
            m.`link`,
            m.`added`,
            m.`is_active`,
            t.`name`
        FROM `{table}` m
        LEFT JOIN `{table}_text` t
            ON m.`id` = t.`item_id`
        AND `language` = '{lang}'
    """.format(table=db.table('menus'), lang=lang)
    cursor.execute(query)
    connection.close()
    menu_items = cursor.fetchall()
    menus = {item['id']: item for item in menu_items}
    parents = {}
    for item in menu_items:
        if item['parent'] is None:
            result[item['id']] = item
            result[item['id']]['items'] = {}
        else:
            if item['parent'] not in parents:
                parents[item['parent']] = []
            parents[item['parent']].append(item['id'])
    def setItems(result):
        for r_menu_id in result:
            if r_menu_id in parents:
                for p_menu_id in parents[r_menu_id]:
                    result[r_menu_id]['items'][p_menu_id] = menus[p_menu_id]
                    result[r_menu_id]['items'][p_menu_id]['items'] = {}
            if result[r_menu_id]['items']:
                setItems(result[r_menu_id]['items'])
    setItems(result)
    if parent is None:
        return result
    elif parent in result:
        return result[parent]
    else:
        return {}

def getMenuItemNames(language):
    db = DB()
    query = """
        SELECT
            m.`id`,
            t.`name`
        FROM `{table}` m
        RIGHT JOIN `{table_text}` t
            ON m.`id` = t.`item_id`
        WHERE t.`language` = %s
    """.format(
        table=db.table('menus'),
        table_text=db.table('menus_text')
    )
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, (language,))
    connection.close()
    menus_names_data = cursor.fetchall()
    return {row['id']: row['name'] for row in menus_names_data} if menus_names_data else {}

def addMenuItem(data):
    db = DB()
    connection = db.getConnection()
    cursor = connection.cursor()
    query = """
        INSERT INTO `{table}` (`parent`, `link`, `added`, `is_active`)
        VALUES (%s, %s, %s, %s)
    """.format(table=db.table('menus'))
    cursor.execute(query, (data.get('parent', None), data.get('link', None), data['added'], data['is_active']))
    values = []
    lang_count = 0
    for language in config.LANGUAGES:
        prop = 'name_' + language
        if prop in data:
            values.extend([
                cursor.lastrowid,
                language,
                data[prop]
            ])
            lang_count += 1
    if values:
        values_placeholders = ', '.join(['(%s, %s, %s)' for _ in range(lang_count)])
        query = """
            INSERT INTO `{table}` (`item_id`, `language`, `name`)
            VALUES {values_placeholders}
        """.format(
            table=db.table('menus_text'),
            values_placeholders=values_placeholders
        )
        cursor.execute(query, values)
    connection.commit()
    connection.close()

def editMenuItem(data):
    db = DB()
    connection = db.getConnection()
    cursor = connection.cursor()
    columns = []
    values = []
    for prop in ('parent', 'link', 'is_active'):
        if prop in data:
            columns.append(prop)
            values.append(data[prop])
    if columns:
        columns = ','.join(['`{column}` = %s'.format(column=column) for column in columns]) if columns else ''
        values.append(data['item_id'])
        query = """
            UPDATE `{table}`
            SET {columns}
            WHERE `id` = %s
        """.format(
            table=db.table('menus'),
            columns=columns
        )
        cursor.execute(query, values)
    values_list = []
    for language in config.LANGUAGES:
        prop = 'name_' + language
        if prop in data:
            values_list.append((
                data['item_id'],
                language,
                data[prop],
                data[prop]
            ))
    if values:
        query = """
            INSERT INTO `{table}` (`item_id`, `language`, `name`)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE `name` = %s
        """.format(table=db.table('menus_text'))
        for values in values_list:
            cursor.execute(query, values)
    connection.commit()
    connection.close()

def deleteMenuItem(item_id):
    db = DB()
    connection = db.getConnection()
    cursor = connection.cursor()
    query = """
        DELETE FROM `{table}`
        WHERE `id` = %s
    """.format(table=db.table('menus'))
    cursor.execute(query, (item_id,))
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
    connection = db.getConnection()
    cursor = connection.cursor()
    query = """
        SELECT
            `id`,
            `parent`,
            `is_active`
        FROM `{table}`
        WHERE `id` = %s
    """.format(table=db.table('categories'))
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
    connection = db.getConnection()
    cursor = connection.cursor()
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

def getCategoryNames(language):
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
    category_names_data = cursor.fetchall()
    return {row['id']: row['name'] for row in category_names_data} if category_names_data else {}

def addCategory(data):
    db = DB()
    query = """
        INSERT INTO `{table}` (`parent`, `added`, `is_active`)
        VALUES (%s, %s, %s)
    """.format(table=db.table('categories'))
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, (data.get('parent', None), data['added'], data['is_active']))
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



#     ########  ########   #######  ########  ##     ##  ######  ########  ######
#     ##     ## ##     ## ##     ## ##     ## ##     ## ##    ##    ##    ##    ##
#     ##     ## ##     ## ##     ## ##     ## ##     ## ##          ##    ##
#     ########  ########  ##     ## ##     ## ##     ## ##          ##     ######
#     ##        ##   ##   ##     ## ##     ## ##     ## ##          ##          ##
#     ##        ##    ##  ##     ## ##     ## ##     ## ##    ##    ##    ##    ##
#     ##        ##     ##  #######  ########   #######   ######     ##     ######



def getProducts(language):
    db = DB()
    connection = db.getConnection()
    cursor = connection.cursor()
    query = """
        SELECT
            p.`id`,
            p.`model`,
            p.`added`,
            p.`is_active`,
            pt.`name`,
            pt.`description`,
            ct.`name` category
        FROM `{table}` p
        LEFT JOIN `{table_t}` pt
            ON p.`id` = pt.`product_id`
        LEFT JOIN `{table_c}` c
            ON p.`category_id` = c.`id`
        LEFT JOIN `{table_ct}` ct
            ON c.`id` = ct.`category_id`
        WHERE pt.`language` = %s
        AND ct.`language` = %s
    """.format(
        table=db.table('products'),
        table_t=db.table('products_text'),
        table_c=db.table('categories'),
        table_ct=db.table('categories_text')
    )
    cursor.execute(query, (language, language))
    products_data = cursor.fetchall()
    if not products_data:
        connection.close()
        return {}
    products = {row['id']: row for row in products_data}
    product_ids = [row['id'] for row in products_data]
    query = """
        SELECT
            pp.`product_id`,
            pp.`value`,
            pt.`name` property
        FROM `{table_pp}` pp
        LEFT JOIN `{table_p}` p
            ON pp.`property_id` = p.`id`
        LEFT JOIN `{table_pt}` pt
            ON p.`id` = pt.`property_id`
        WHERE pp.`product_id` IN %s
        AND pp.`language` = %s
        AND pt.`language` = %s
    """.format(
        table_pp=db.table('products_properties'),
        table_p=db.table('properties'),
        table_pt=db.table('properties_text'),
    )
    cursor.execute(query, (product_ids, language, language))
    connection.close()
    product_properties_data = cursor.fetchall()
    for row in product_properties_data:
        if row['product_id'] in products:
            if 'properties' not in products[row['product_id']]: products[row['product_id']]['properties'] = {}
            products[row['product_id']]['properties'][row['property']] = row['value']
    return products

def addProduct(data):
    db = DB()
    connection = db.getConnection()
    cursor = connection.cursor()
    query = """
        INSERT INTO `{table}` (`category_id`, `model`, `price`, `added`, `is_active`)
        VALUES (%s, %s, %s, %s, %s)
    """.format(table=db.table('products'))
    cursor.execute(query, (data['category_id'], data['model'], data['price'], data['added'], data['is_active']))
    product_id = cursor.lastrowid
    for language in config.LANGUAGES:
        prop_name = 'name_' + language
        prop_description = 'description_' + language
        if prop_name in data or prop_description in data:
            query = """
                INSERT INTO `{table}` (`product_id`, `language`, `name`, `description`)
                VALUES (%s, %s, %s, %s)
            """.format(table=db.table('products_text'))
            cursor.execute(query, (product_id, language, data.get(prop_name, None), data.get(prop_description, None)))
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
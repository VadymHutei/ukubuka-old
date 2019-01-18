from db import DB

def getMenus(lang):
    db = DB()
    table = db.table('menus')
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

def addMenuItem(**data):
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
    table = db.table('menus')
    query = """
        INSERT INTO `{table}` ({columns})
        VALUES ({placeholders})
    """.format(
        table=table,
        columns=', '.join(map(lambda x: '`' + x + '`', columns)),
        placeholders=', '.join(placeholders)
    )
    connection = db.getConnection()
    cursor = connection.cursor()
    cursor.execute(query, values)
    table = db.table('menus_text')
    columns = ['item_id', 'language', 'name']
    values = [
        [cursor.lastrowid, 'ukr', data['name_ukr']],
        [cursor.lastrowid, 'eng', data['name_eng']]
    ]
    query = """
        INSERT INTO `{table}` (`item_id`, `language`, `name`)
        VALUES (%s, %s, %s)
    """.format(table=table)
    cursor.executemany(query, values)
    connection.commit()
    connection.close()
    return True

def editMenuItem(**data):
    return False
    # columns = ['menu', 'is_active']
    # values = [data['menu'], data['is_active']]
    # placeholders = ['%s', '%s']
    # if 'parent' in data:
    #     columns.append('parent')
    #     values.append(data['parent'])
    #     placeholders.append('%s')
    # if 'link' in data:
    #     columns.append('link')
    #     values.append(data['link'])
    #     placeholders.append('%s')
    # db = DB()
    # table = db.table('menus')
    # query = """
    #     UPDATE TABLE `{table}`
    #     SET 
    #     WHERE `id` = {item_id}
    #     INSERT INTO `{table}` ({columns})
    #     VALUES ({placeholders})
    # """.format(
    #     table=table,
    #     columns=', '.join(map(lambda x: '`' + x + '`', columns)),
    #     placeholders=', '.join(placeholders)
    # )
    # connection = db.getConnection()
    # cursor = connection.cursor()
    # cursor.execute(query, values)
    # table = db.table('menus_text')
    # columns = ['item_id', 'language', 'name']
    # values = [
    #     [cursor.lastrowid, 'ukr', data['name_ukr']],
    #     [cursor.lastrowid, 'eng', data['name_eng']]
    # ]
    # query = """
    #     INSERT INTO `{table}` (`item_id`, `language`, `name`)
    #     VALUES (%s, %s, %s)
    # """.format(table=table)
    # cursor.executemany(query, values)
    # connection.commit()
    # connection.close()
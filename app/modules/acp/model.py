from db import DB

def getMenu(lang):
    db = DB()
    table = db.table('menus')
    query = """
        SELECT `name`
        FROM {table} m
        LEFT JOIN {table}_text t
            ON m.id = t.item_id
        WHERE `menu` = 'acp_main'
        AND language = '{lang}'
    """.format(table=db.table('menus'), lang=lang)
    return []

def getMenusList():
    db = DB()
    table = db.table('menus')
    query = """
        SELECT `menu`
        FROM {table} m
        GROUP BY `menu`
    """.format(table=db.table('menus'))
    menus = db.getAll(query)
    result = []
    for menu in menus:
        result.append(menu['menu'])
    return result
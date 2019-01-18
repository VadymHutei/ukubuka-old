import re

def validMenuItemID(item_id):
    return bool(re.fullmatch(r'\d{1,4}', item_id))

def validMenuName(name):
    return name == '' or re.fullmatch(r'\w{1,32}', name)

def validMenuItemName(name):
    return name == '' or re.fullmatch(r'\w{1,64}', name)

def validMenuItemLink(link):
    return bool(re.fullmatch(r'[\w:./]{1,128}', link))

def prepareMenuItemData(form):
    item_id = form.get('id')
    menu = form.get('menu')
    parent = form.get('parent')
    name_ukr = form.get('name_ukr')
    name_eng = form.get('name_eng')
    link = form.get('link')
    is_active = form.get('is_active', 'off')
    if menu is None or parent is None or name_ukr is None or name_eng is None or link is None: return False
    result = {
        'menu': menu if validMenuName(menu) else '',
        'name_ukr': name_ukr if validMenuItemName(name_ukr) else '',
        'name_eng': name_eng if validMenuItemName(name_eng) else '',
        'is_active': 'Y' if is_active == 'on' else 'N'
    }
    if validMenuItemID(item_id): result['id'] = item_id
    if validMenuItemID(parent): result['parent'] = parent
    if validMenuItemLink(link): result['link'] = link
    return result
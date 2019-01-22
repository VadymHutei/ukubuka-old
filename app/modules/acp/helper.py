import re

def validMenuItemID(item_id):
    if isinstance(item_id, str):
        return bool(re.fullmatch(r'\d{1,4}', item_id))
    return False

def validMenuName(name):
    if isinstance(name, str):
        return name == '' or re.fullmatch(r'\w{1,32}', name)
    return False

def validMenuItemName(name):
    if isinstance(name, str):
        return name == '' or re.fullmatch(r'\w{1,64}', name)
    return False

def validMenuItemLink(link):
    if isinstance(link, str):
        return bool(re.fullmatch(r'[\w:./]{1,128}', link))
    return False

def prepareMenuItemFormData(form):
    item_id = form.get('id')
    menu = form.get('menu')
    parent = form.get('parent')
    name_ukr = form.get('name_ukr')
    name_eng = form.get('name_eng')
    link = form.get('link')
    is_active = form.get('is_active', 'off')
    result = {}
    if item_id: result['item_id'] = item_id
    if menu: result['menu'] = menu
    if parent: result['parent'] = parent
    if name_ukr: result['name_ukr'] = name_ukr
    if name_eng: result['name_eng'] = name_eng
    if link: result['link'] = link
    result['is_active'] = 'Y' if is_active == 'on' else 'N'
    return result

def validAddMenuItemData(data):
    if 'menu' not in data or not validMenuName(data['menu']): return False
    if 'name_ukr' not in data or not validMenuItemName(data['name_ukr']): return False
    if 'name_eng' not in data or not validMenuItemName(data['name_eng']): return False
    if 'link' in data and not validMenuItemLink(data['link']): return False
    if 'parent' in data and not validMenuItemID(data['parent']): return False
    if 'is_active' in data and data['is_active'] not in ['Y', 'N']: return False
    return True

def validEditMenuItemData(data):
    if 'item_id' not in data or not validMenuItemID(data['item_id']): return False
    if 'menu' in data and not validMenuName(data['menu']): return False
    if 'name_ukr' in data and not validMenuItemName(data['name_ukr']): return False
    if 'name_eng' in data and not validMenuItemName(data['name_eng']): return False
    if 'link' in data and not validMenuItemLink(data['link']): return False
    if 'parent' in data and not validMenuItemID(data['parent']): return False
    if 'is_active' in data and data['is_active'] not in ['Y', 'N']: return False
    return True

def prepareAddMenuItemData(data):
    result = {
        'menu': data['menu'],
        'name_ukr': data['name_ukr'],
        'name_eng': data['name_eng'],
        'is_active': data['is_active']
    }
    if 'link' in data: result['link'] = data['link']
    if 'parent' in data: result['parent'] = data['parent']
    return result

def prepareEditMenuItemData(data):
    result = {'item_id': data['item_id']}
    if 'menu' in data: result['menu'] = data['menu']
    if 'name_ukr' in data: result['name_ukr'] = data['name_ukr']
    if 'name_eng' in data: result['name_eng'] = data['name_eng']
    if 'link' in data: result['link'] = data['link']
    if 'parent' in data: result['parent'] = data['parent']
    if 'is_active' in data: result['is_active'] = data['is_active']
    return result
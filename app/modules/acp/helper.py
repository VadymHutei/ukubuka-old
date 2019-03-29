from datetime import datetime
import re
import config
import modules.validation as validation
import modules.auth as auth



#     ##     ## ######## ##    ## ##     ##
#     ###   ### ##       ###   ## ##     ##
#     #### #### ##       ####  ## ##     ##
#     ## ### ## ######   ## ## ## ##     ##
#     ##     ## ##       ##  #### ##     ##
#     ##     ## ##       ##   ### ##     ##
#     ##     ## ######## ##    ##  #######



def prepareMenuItemFormData(form):
    result = {}
    item_id = form.get('id')
    if item_id: result['item_id'] = item_id
    parent = form.get('parent')
    if parent: result['parent'] = parent
    for language in config.LANGUAGES:
        field = 'name_' + language
        name = form.get(field)
        if name: result[field] = name
    link = form.get('link')
    if link: result['link'] = link
    is_active = form.get('is_active', 'off')
    result['is_active'] = 'Y' if is_active == 'on' else 'N'
    return result

def validAddMenuItemData(data):
    if 'parent' in data and not (validation.menuItemID(data['parent']) or data['parent'] is None): return False
    for language in config.LANGUAGES:
        prop = 'name_' + language
        if prop in data and not validation.menuItemName(data[prop]): return False
    if 'link' in data and not validation.menuItemLink(data['link']): return False
    if 'is_active' in data and data['is_active'] not in ('Y', 'N'): return False
    return True

def validEditMenuItemData(data):
    if 'item_id' not in data or not validation.menuItemID(data['item_id']): return False
    if 'parent' in data and not validation.menuItemID(data['parent']): return False
    for language in config.LANGUAGES:
        prop = 'name_' + language
        if prop in data and not validation.menuItemName(data[prop]): return False
    if 'link' in data and not validation.menuItemLink(data['link']): return False
    if 'is_active' in data and data['is_active'] not in ('Y', 'N'): return False
    return True

def prepareAddMenuItemData(data):
    result = {
        'added': datetime.now(),
        'is_active': data['is_active']
    }
    for language in config.LANGUAGES:
        prop = 'name_' + language
        if prop in data and data[prop]: result[prop] = data[prop]
    if 'parent' in data: result['parent'] = data['parent']
    if 'link' in data: result['link'] = data['link']
    return result

def prepareEditMenuItemData(data):
    result = {'item_id': data['item_id']}
    for language in config.LANGUAGES:
        prop = 'name_' + language
        result[prop] = data[prop] if prop in data and data[prop] else None
    result['parent'] = data['parent'] if 'parent' in data else None
    result['link'] = data['link'] if 'link' in data else None
    if 'is_active' in data: result['is_active'] = data['is_active']
    return result



#      ######     ###    ######## ########  ######    #######  ########  #### ########  ######
#     ##    ##   ## ##      ##    ##       ##    ##  ##     ## ##     ##  ##  ##       ##    ##
#     ##        ##   ##     ##    ##       ##        ##     ## ##     ##  ##  ##       ##
#     ##       ##     ##    ##    ######   ##   #### ##     ## ########   ##  ######    ######
#     ##       #########    ##    ##       ##    ##  ##     ## ##   ##    ##  ##             ##
#     ##    ## ##     ##    ##    ##       ##    ##  ##     ## ##    ##   ##  ##       ##    ##
#      ######  ##     ##    ##    ########  ######    #######  ##     ## #### ########  ######



def prepareCategoryFormData(form):
    result = {}
    category_id = form.get('id')
    if category_id: result['id'] = category_id
    parent = form.get('parent')
    result['parent'] = parent if parent else None
    for language in config.LANGUAGES:
        field = 'name_' + language
        name = form.get(field)
        if name: result[field] = name
    is_active = form.get('is_active', 'off')
    result['is_active'] = 'Y' if is_active == 'on' else 'N'
    return result

def validAddCategoryData(data):
    if 'parent' not in data or not (validation.categoryID(data['parent']) or data['parent'] is None): return False
    if 'is_active' in data and data['is_active'] not in ('Y', 'N'): return False
    for language in config.LANGUAGES:
        prop = 'name_' + language
        if prop in data and not validation.categoryName(data[prop]): return False
    if 'name_eng' in data and not validation.categoryName(data['name_eng']): return False
    return True

def prepareAddCategoryData(data):
    result = {
        'parent': data['parent'],
        'added': datetime.now(),
        'is_active': data['is_active']
    }
    for language in config.LANGUAGES:
        prop = 'name_' + language
        if prop in data and data[prop]: result[prop] = data[prop]
    return result

def validEditCategoryData(data):
    if 'id' not in data or not validation.categoryID(data['id']): return False
    if 'parent' in data and not (validation.categoryID(data['parent']) or data['parent'] is None): return False
    if 'is_active' in data and data['is_active'] not in ('Y', 'N'): return False
    for language in config.LANGUAGES:
        prop = 'name_' + language
        if prop in data and not validation.categoryName(data[prop]): return False
    return True

def prepareEditCategoryData(data):
    result = {'id': data['id']}
    if 'parent' in data and (data['parent'] or data['parent'] is None): result['parent'] = data['parent']
    for language in config.LANGUAGES:
        prop = 'name_' + language
        if prop in data and data[prop]: result[prop] = data[prop]
    if 'is_active' in data and data['is_active']: result['is_active'] = data['is_active']
    return result



#     ##     ##  ######  ######## ########   ######
#     ##     ## ##    ## ##       ##     ## ##    ##
#     ##     ## ##       ##       ##     ## ##
#     ##     ##  ######  ######   ########   ######
#     ##     ##       ## ##       ##   ##         ##
#     ##     ## ##    ## ##       ##    ##  ##    ##
#      #######   ######  ######## ##     ##  ######



def prepareUserFormData(form):
    result = {}
    user_id = form.get('id')
    group_id = form.get('group_id')
    first_name = form.get('first_name')
    patronymic = form.get('patronymic')
    last_name = form.get('last_name')
    phone_number = form.get('phone_number')
    phone_numbers = form.getlist('phone_numbers[]')
    email = form.get('email')
    emails = form.getlist('emails[]')
    is_active = form.get('is_active')
    password = form.get('password')
    if user_id: result['user_id'] = user_id
    if group_id: result['group_id'] = group_id
    if first_name: result['first_name'] = first_name
    if patronymic: result['patronymic'] = patronymic
    if last_name: result['last_name'] = last_name
    if phone_number: result['phone_number'] = phone_number
    if phone_numbers: result['phone_numbers'] = phone_numbers
    if email: result['email'] = email
    if emails: result['emails'] = emails
    result['is_active'] = 'Y' if is_active == 'on' else 'N'
    if password: result['password'] = password
    return result

def validAddUserData(data):
    if 'group_id' not in data or not validation.usersGroupID(data['group_id']): return False
    if 'is_active' not in data or data['is_active'] not in ('Y', 'N'): return False
    if 'first_name' in data and not validation.userName(data['first_name']): return False
    if 'patronymic' in data and not validation.userName(data['patronymic']): return False
    if 'last_name' in data and not validation.userName(data['last_name']): return False
    if 'phone_number' in data and not validation.phoneNumber(data['phone_number']): return False
    if 'email' in data and not validation.email(data['email']): return False
    if 'password' in data and not validation.password(data['password']): return False
    return True

def prepareAddUserData(data):
    result = {
        'group_id': data['group_id'],
        'is_active': data['is_active']
    }
    if 'first_name' in data and data['first_name']: result['first_name'] = data['first_name']
    if 'patronymic' in data and data['patronymic']: result['patronymic'] = data['patronymic']
    if 'last_name' in data and data['last_name']: result['last_name'] = data['last_name']
    if 'phone_number' in data and data['phone_number']: result['phone_number'] = data['phone_number']
    if 'email' in data and data['email']: result['email'] = data['email']
    if 'password' in data and data['password']:
        salt = auth.generateSalt()
        result['salt'] = salt
        result['password_hash'] = auth.hashPassword(data['password'], salt)
    result['added'] = datetime.now()
    return result

def validEditUserData(data):
    if 'user_id' not in data or not validation.userID(data['user_id']): return False
    if 'group_id' in data and not validation.usersGroupID(data['group_id']): return False
    if 'is_active' in data and data['is_active'] not in ('Y', 'N'): return False
    if 'first_name' in data and not validation.userName(data['first_name']): return False
    if 'patronymic' in data and not validation.userName(data['patronymic']): return False
    if 'last_name' in data and not validation.userName(data['last_name']): return False
    if 'phone_number' in data and not validation.phoneNumber(data['phone_number']): return False
    if 'phone_numbers' in data:
        for phone_number in data['phone_numbers']:
            if not validation.phoneNumber(phone_number): return False
    if 'email' in data and not validation.email(data['email']): return False
    if 'emails' in data:
        for email in data['emails']:
            if not validation.email(email): return False
    if 'password' in data and not validation.password(data['password']): return False
    return True

def prepareEditUserData(data):
    result = {'user_id': data['user_id']}
    if 'group_id' in data: result['group_id'] = data['group_id']
    if 'first_name' in data and data['first_name']: result['first_name'] = data['first_name']
    if 'patronymic' in data and data['patronymic']: result['patronymic'] = data['patronymic']
    if 'last_name' in data and data['last_name']: result['last_name'] = data['last_name']
    if 'phone_number' in data and data['phone_number']: result['phone_number'] = data['phone_number']
    if 'phone_numbers' in data and data['phone_numbers']:
        result['phone_numbers'] = []
        for phone_number in data['phone_numbers']:
            if phone_number:
                result['phone_numbers'].append(phone_number)
    if 'email' in data and data['email']: result['email'] = data['email']
    if 'emails' in data and data['emails']:
        result['emails'] = []
        for email in data['emails']:
            if email:
                result['emails'].append(email)
    if 'is_active' in data: result['is_active'] = data['is_active']
    if 'password' in data and data['password']:
        salt = auth.generateSalt()
        result['salt'] = salt
        result['password'] = auth.hashPassword(data['password'], salt)
    return result

def validAddUserPhoneNumberData(data):
    if 'user_id' not in data or not validation.userID(data['user_id']): return False
    if 'phone_number' not in data or not validation.phoneNumber(data['phone_number']) or not data['phone_number']: return False
    return True

def prepareAddUserPhoneNumberData(data):
    return {
        'user_id': data['user_id'],
        'phone_number': data['phone_number']
    }

def validAddUserEmailData(data):
    if 'user_id' not in data or not validation.userID(data['user_id']): return False
    if 'email' not in data or not validation.email(data['email']) or not data['email']: return False
    return True

def prepareAddUserEmailData(data):
    return {
        'user_id': data['user_id'],
        'email': data['email']
    }
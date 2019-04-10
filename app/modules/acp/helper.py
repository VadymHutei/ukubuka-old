from datetime import datetime
import re
import config
import common
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
    if item_id: result['id'] = item_id
    parent = form.get('parent')
    if parent: result['parent'] = parent
    for language in config.LANGUAGES:
        field = 'name_' + language
        name = form.get(field)
        if name: result[field] = name
    link = form.get('link')
    if link: result['link'] = link
    order = form.get('order')
    if order: result['order'] = order
    result['is_active'] = 'Y' if form.get('is_active', 'off') == 'on' else 'N'
    return result

def validAddMenuItemData(data):
    if 'parent' in data and not validation.menuItemID(data['parent']): return False
    for language in config.LANGUAGES:
        prop = 'name_' + language
        if prop in data and not validation.menuItemName(data[prop]): return False
    if 'link' in data and not validation.menuItemLink(data['link']): return False
    if 'order' in data and not validation.order(data['order']): return False
    if 'is_active' not in data or data['is_active'] not in ('Y', 'N'): return False
    return True

def prepareAddMenuItemData(data):
    result = {'added': datetime.now()}
    for language in config.LANGUAGES:
        prop = 'name_' + language
        result[prop] = data[prop] if prop in data and data[prop] else None
    result['parent'] = int(data['parent']) if 'parent' in data else None
    result['link'] = data['link'] if 'link' in data else None
    result['order'] = int(data['order']) if 'order' in data and data['order'] else 100
    result['is_active'] = data['is_active'] if 'is_active' in data and data['is_active'] else 'Y'
    return result

def validEditMenuItemData(data):
    if 'id' not in data or not validation.menuItemID(data['id']): return False
    if 'parent' in data and not validation.menuItemID(data['parent']): return False
    for language in config.LANGUAGES:
        prop = 'name_' + language
        if prop in data and not validation.menuItemName(data[prop]): return False
    if 'link' in data and not validation.menuItemLink(data['link']): return False
    if 'order' in data and not validation.order(data['order']): return False
    if 'is_active' not in data or data['is_active'] not in ('Y', 'N'): return False
    return True

def prepareEditMenuItemData(data):
    result = {'id': int(data['id'])}
    for language in config.LANGUAGES:
        prop = 'name_' + language
        result[prop] = data[prop] if prop in data and data[prop] else None
    result['parent'] = int(data['parent']) if 'parent' in data else None
    result['link'] = data['link'] if 'link' in data else None
    result['order'] = int(data['order']) if 'order' in data and data['order'] else 100
    result['is_active'] = data['is_active'] if 'is_active' in data and data['is_active'] else 'Y'
    return result



#      ######  ##     ## ########  ########  ######## ##    ##  ######  #### ########  ######
#     ##    ## ##     ## ##     ## ##     ## ##       ###   ## ##    ##  ##  ##       ##    ##
#     ##       ##     ## ##     ## ##     ## ##       ####  ## ##        ##  ##       ##
#     ##       ##     ## ########  ########  ######   ## ## ## ##        ##  ######    ######
#     ##       ##     ## ##   ##   ##   ##   ##       ##  #### ##        ##  ##             ##
#     ##    ## ##     ## ##    ##  ##    ##  ##       ##   ### ##    ##  ##  ##       ##    ##
#      ######   #######  ##     ## ##     ## ######## ##    ##  ######  #### ########  ######



def prepareCurrencyFormData(form):
    result = {}
    code = form.get('code')
    if code: result['code'] = code
    new_code = form.get('new_code')
    if new_code: result['new_code'] = new_code
    name = form.get('name')
    if name: result['name'] = name
    symbol = form.get('symbol')
    if symbol: result['symbol'] = symbol
    order = form.get('order')
    if order: result['order'] = order
    result['is_active'] = 'Y' if form.get('is_active', 'off') == 'on' else 'N'
    return result

def validAddCurrencyData(data):
    if 'code' not in data or not validation.currencyCode(data['code']): return False
    if 'name' in data and not validation.currencyName(data['name']): return False
    if 'symbol' in data and not validation.currencySymbol(data['symbol']): return False
    if 'order' in data and not validation.order(data['order']): return False
    if 'is_active' not in data or data['is_active'] not in ('Y', 'N'): return False
    return True

def prepareAddCurrencyData(data):
    result = {
        'code': data['code'].upper(),
        'added': datetime.now()
        }
    result['name'] = data['name'] if 'name' in data else None
    result['symbol'] = data['symbol'] if 'symbol' in data else None
    result['order'] = int(data['order']) if 'order' in data and data['order'] else 100
    result['is_active'] = data['is_active'] if 'is_active' in data and data['is_active'] else 'Y'
    return result

def validEditCurrencyData(data):
    if 'code' not in data or not validation.currencyCode(data['code']): return False
    if 'new_code' in data and not validation.currencyCode(data['new_code']): return False
    if 'name' in data and not validation.currencyName(data['name']): return False
    if 'symbol' in data and not validation.currencySymbol(data['symbol']): return False
    if 'order' in data and not validation.order(data['order']): return False
    if 'is_active' not in data or data['is_active'] not in ('Y', 'N'): return False
    return True

def prepareEditCurrencyData(data):
    result = {'code': data['code'].upper()}
    result['new_code'] = data['new_code'].upper() if 'new_code' in data else data['code'].upper()
    result['name'] = data['name'] if 'name' in data else None
    result['symbol'] = data['symbol'] if 'symbol' in data else None
    result['order'] = int(data['order']) if 'order' in data and data['order'] else 100
    result['is_active'] = data['is_active'] if 'is_active' in data and data['is_active'] else 'Y'
    return result



#     ##          ###    ##    ##  ######   ##     ##    ###     ######   ########  ######
#     ##         ## ##   ###   ## ##    ##  ##     ##   ## ##   ##    ##  ##       ##    ##
#     ##        ##   ##  ####  ## ##        ##     ##  ##   ##  ##        ##       ##
#     ##       ##     ## ## ## ## ##   #### ##     ## ##     ## ##   #### ######    ######
#     ##       ######### ##  #### ##    ##  ##     ## ######### ##    ##  ##             ##
#     ##       ##     ## ##   ### ##    ##  ##     ## ##     ## ##    ##  ##       ##    ##
#     ######## ##     ## ##    ##  ######    #######  ##     ##  ######   ########  ######



def prepareLanguageFormData(form):
    result = {}
    code = form.get('code')
    if code: result['code'] = code
    new_code = form.get('new_code')
    if new_code: result['new_code'] = new_code
    name = form.get('name')
    if name: result['name'] = name
    result['is_default'] = 'Y' if form.get('is_default', 'off') == 'on' else 'N'
    order = form.get('order')
    if order: result['order'] = order
    result['is_active'] = 'Y' if form.get('is_active', 'off') == 'on' else 'N'
    return result

def validAddLanguageData(data):
    if 'code' not in data or not validation.currencyCode(data['code']): return False
    if 'name' in data and not validation.currencyName(data['name']): return False
    if 'is_default' not in data or data['is_default'] not in ('Y', 'N'): return False
    if 'order' in data and not validation.order(data['order']): return False
    if 'is_active' not in data or data['is_active'] not in ('Y', 'N'): return False
    return True

def prepareAddLanguageData(data):
    result = {
        'code': data['code'].lower(),
        'added': datetime.now()
        }
    result['name'] = data['name'] if 'name' in data else None
    result['is_default'] = data['is_default'] if 'is_default' in data and data['is_default'] else 'N'
    result['order'] = int(data['order']) if 'order' in data and data['order'] else 100
    result['is_active'] = data['is_active'] if 'is_active' in data and data['is_active'] else 'Y'
    return result

def validEditLanguageData(data):
    if 'code' not in data or not validation.currencyCode(data['code']): return False
    if 'new_code' in data and not validation.currencyCode(data['new_code']): return False
    if 'name' in data and not validation.currencyName(data['name']): return False
    if 'is_default' not in data or data['is_default'] not in ('Y', 'N'): return False
    if 'order' in data and not validation.order(data['order']): return False
    if 'is_active' not in data or data['is_active'] not in ('Y', 'N'): return False
    return True

def prepareEditLanguageData(data):
    result = {'code': data['code'].lower()}
    result['new_code'] = data['new_code'].lower() if 'new_code' in data else data['code'].lower()
    result['name'] = data['name'] if 'name' in data else None
    result['is_default'] = data['is_default'] if 'is_default' in data and data['is_default'] else 'N'
    result['order'] = int(data['order']) if 'order' in data and data['order'] else 100
    result['is_active'] = data['is_active'] if 'is_active' in data and data['is_active'] else 'Y'
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
    for language in config.LANGUAGES:
        field = 'name_' + language
        name = form.get(field)
        if name: result[field] = name
    parent = form.get('parent')
    if parent: result['parent'] = parent
    order = form.get('order')
    if order: result['order'] = order
    result['is_active'] = 'Y' if form.get('is_active', 'off') == 'on' else 'N'
    return result

def validAddCategoryData(data):
    for language in config.LANGUAGES:
        prop = 'name_' + language
        if prop in data and not validation.categoryName(data[prop]): return False
    if 'parent' in data and not validation.categoryID(data['parent']): return False
    if 'order' in data and not validation.order(data['order']): return False
    if 'is_active' not in data or data['is_active'] not in ('Y', 'N'): return False
    return True

def prepareAddCategoryData(data):
    result = {'added': datetime.now()}
    for language in config.LANGUAGES:
        prop = 'name_' + language
        result[prop] = data[prop] if prop in data and data[prop] else None
    result['parent'] = int(data['parent']) if 'parent' in data and data['parent'] else None
    result['order'] = int(data['order']) if 'order' in data and data['order'] else 100
    result['is_active'] = data['is_active'] if 'is_active' in data and data['is_active'] else 'Y'
    return result

def validEditCategoryData(data):
    if 'id' not in data or not validation.categoryID(data['id']): return False
    for language in config.LANGUAGES:
        prop = 'name_' + language
        if prop in data and not validation.categoryName(data[prop]): return False
    if 'parent' in data and not validation.categoryID(data['parent']): return False
    if 'order' in data and not validation.order(data['order']): return False
    if 'is_active' not in data or data['is_active'] not in ('Y', 'N'): return False
    return True

def prepareEditCategoryData(data):
    result = {'id': int(data['id'])}
    for language in config.LANGUAGES:
        prop = 'name_' + language
        result[prop] = data[prop] if prop in data and data[prop] else None
    result['parent'] = int(data['parent']) if 'parent' in data and data['parent'] else None
    result['order'] = int(data['order']) if 'order' in data and data['order'] else 100
    result['is_active'] = data['is_active'] if 'is_active' in data and data['is_active'] else 'Y'
    return result



#     ########  ########   #######  ########  ##     ##  ######  ########  ######
#     ##     ## ##     ## ##     ## ##     ## ##     ## ##    ##    ##    ##    ##
#     ##     ## ##     ## ##     ## ##     ## ##     ## ##          ##    ##
#     ########  ########  ##     ## ##     ## ##     ## ##          ##     ######
#     ##        ##   ##   ##     ## ##     ## ##     ## ##          ##          ##
#     ##        ##    ##  ##     ## ##     ## ##     ## ##    ##    ##    ##    ##
#     ##        ##     ##  #######  ########   #######   ######     ##     ######



def prepareProductFormData(form):
    result = {}
    model = form.get('model')
    if model: result['model'] = model
    for language in config.LANGUAGES:
        field = 'name_' + language
        name = form.get(field)
        if name: result[field] = name
    for language in config.LANGUAGES:
        field = 'description_' + language
        description = form.get(field)
        if description: result[field] = description
    category_id = form.get('category_id')
    price = form.get('price')
    if price: result['price'] = price
    if category_id: result['category_id'] = category_id
    result['is_active'] = 'Y' if form.get('is_active', 'off') == 'on' else 'N'
    return result

def validAddProductData(data):
    if 'model' in data and not validation.productModel(data['model']): return False
    for language in config.LANGUAGES:
        prop = 'name_' + language
        if prop in data and not validation.productName(data[prop]): return False
    for language in config.LANGUAGES:
        prop = 'description_' + language
        if prop in data and not validation.productName(data[prop]): return False
    if 'category_id' in data and not (validation.categoryID(data['category_id']) or data['category_id'] is None): return False
    if 'price' in data and not validation.price(data['price']): return False
    if 'is_active' not in data or data['is_active'] not in ('Y', 'N'): return False
    return True

def prepareAddProductData(data):
    result = {'added': datetime.now()}
    result['category_id'] = int(data['category_id']) if 'category_id' in data and data['category_id'] else None
    result['model'] = data['model'] if 'model' in data and data['model'] else None
    for language in config.LANGUAGES:
        prop = 'name_' + language
        result[prop] = data[prop] if prop in data and data[prop] else None
    for language in config.LANGUAGES:
        prop = 'description_' + language
        result[prop] = data[prop] if prop in data and data[prop] else None
    result['price'] = common.parsePrice(data['price']) if 'price' in data and data['price'] else None
    result['is_active'] = data['is_active'] if 'is_active' in data and data['is_active'] else 'Y'
    return result



#      ######  ##     ##    ###    ########     ###     ######  ######## ######## ########  ####  ######  ######## ####  ######
#     ##    ## ##     ##   ## ##   ##     ##   ## ##   ##    ##    ##    ##       ##     ##  ##  ##    ##    ##     ##  ##    ##
#     ##       ##     ##  ##   ##  ##     ##  ##   ##  ##          ##    ##       ##     ##  ##  ##          ##     ##  ##
#     ##       ######### ##     ## ########  ##     ## ##          ##    ######   ########   ##   ######     ##     ##  ##
#     ##       ##     ## ######### ##   ##   ######### ##          ##    ##       ##   ##    ##        ##    ##     ##  ##
#     ##    ## ##     ## ##     ## ##    ##  ##     ## ##    ##    ##    ##       ##    ##   ##  ##    ##    ##     ##  ##    ##
#      ######  ##     ## ##     ## ##     ## ##     ##  ######     ##    ######## ##     ## ####  ######     ##    ####  ######



def prepareCharacteristicFormData(form):
    result = {}
    characteristic_id = form.get('id')
    if characteristic_id: result['id'] = characteristic_id
    for language in config.LANGUAGES:
        field = 'name_' + language
        name = form.get(field)
        if name: result[field] = name
    order = form.get('order')
    if order: result['order'] = order
    result['is_active'] = 'Y' if form.get('is_active', 'off') == 'on' else 'N'
    return result

def validAddCharacteristicData(data):
    for language in config.LANGUAGES:
        prop = 'name_' + language
        if prop in data and not validation.characteristicName(data[prop]): return False
    if 'order' in data and not validation.order(data['order']): return False
    if 'is_active' not in data or data['is_active'] not in ('Y', 'N'): return False
    return True

def prepareAddCharacteristicData(data):
    result = {'added': datetime.now()}
    for language in config.LANGUAGES:
        prop = 'name_' + language
        result[prop] = data[prop] if prop in data and data[prop] else None
    result['order'] = int(data['order']) if 'order' in data and data['order'] else 100
    result['is_active'] = data['is_active'] if 'is_active' in data and data['is_active'] else 'Y'
    return result

def validEditCharacteristicData(data):
    if 'id' not in data or not validation.characteristicID(data['id']): return False
    for language in config.LANGUAGES:
        prop = 'name_' + language
        if prop in data and not validation.characteristicName(data[prop]): return False
    if 'order' in data and not validation.order(data['order']): return False
    if 'is_active' not in data or data['is_active'] not in ('Y', 'N'): return False
    return True

def prepareEditCharacteristicData(data):
    result = {'id': int(data['id'])}
    for language in config.LANGUAGES:
        prop = 'name_' + language
        result[prop] = data[prop] if prop in data and data[prop] else None
    result['order'] = int(data['order']) if 'order' in data and data['order'] else 100
    result['is_active'] = data['is_active'] if 'is_active' in data and data['is_active'] else 'Y'
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
    if 'is_active' not in data or data['is_active'] not in ('Y', 'N'): return False
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
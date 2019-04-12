import re

def phoneNumber(phone_number):
    if isinstance(phone_number, str):
        return re.fullmatch(r'[0-9+() -]{9,64}', phone_number)
    if isinstance(phone_number, int):
        return 9 <= len(str(phone_number)) <= 32
    return False

def email(email):
    if isinstance(email, str):
        return re.fullmatch(r'[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+', email)
    return False

def settingsProperty(prop):
    if isinstance(prop, str):
        return re.fullmatch(r'[\w. -]{1,64}', prop)
    return False

def password(prop):
    if isinstance(prop, str):
        return re.fullmatch(r'[\w\W]{3,64}', prop)
    return False

def sessionId(session_id):
    if isinstance(session_id, str):
        return bool(re.fullmatch(r'[0-9a-z]{64}', session_id))
    return False

def price(price):
    if isinstance(price, str):
        return re.fullmatch(r'[0-9 .,]{1,16}', price)
    if isinstance(price, int):
        return 1 <= len(str(price)) <= 6
    if isinstance(price, float):
        return 1 <= len(str(price)) <= 9
    return False

def order(order):
    if isinstance(order, str):
        return re.fullmatch(r'[0-9]{1,4}', order)
    if isinstance(order, int):
        return 1 <= len(str(order)) <= 4
    return False

#     ##     ## ######## ##    ## ##     ##
#     ###   ### ##       ###   ## ##     ##
#     #### #### ##       ####  ## ##     ##
#     ## ### ## ######   ## ## ## ##     ##
#     ##     ## ##       ##  #### ##     ##
#     ##     ## ##       ##   ### ##     ##
#     ##     ## ######## ##    ##  #######

def menuItemID(item_id):
    if isinstance(item_id, str):
        return bool(re.fullmatch(r'[0-9]{1,4}', item_id))
    if isinstance(item_id, int):
        return 1 <= len(str(item_id)) <= 4
    return False

def menuName(name):
    if isinstance(name, str):
        return re.fullmatch(r'\w{1,32}', name)
    return False

def menuItemName(name):
    if isinstance(name, str):
        return re.fullmatch(r'[0-9A-Za-zА-Яа-яЯєЄіІїЇёЁҐґ _-]{1,64}', name)
    return False

def menuItemLink(link):
    if isinstance(link, str):
        return bool(re.fullmatch(r'[\w:./]{1,128}', link))
    return False

#      ######  ##     ## ########  ########  ######## ##    ##  ######  #### ########  ######
#     ##    ## ##     ## ##     ## ##     ## ##       ###   ## ##    ##  ##  ##       ##    ##
#     ##       ##     ## ##     ## ##     ## ##       ####  ## ##        ##  ##       ##
#     ##       ##     ## ########  ########  ######   ## ## ## ##        ##  ######    ######
#     ##       ##     ## ##   ##   ##   ##   ##       ##  #### ##        ##  ##             ##
#     ##    ## ##     ## ##    ##  ##    ##  ##       ##   ### ##    ##  ##  ##       ##    ##
#      ######   #######  ##     ## ##     ## ######## ##    ##  ######  #### ########  ######

def currencyCode(code):
    if isinstance(code, str):
        return re.fullmatch(r'[a-zA-Z]{3}', code)
    return False

def currencyName(name):
    if isinstance(name, str):
        return re.fullmatch(r'[0-9A-Za-zА-Яа-яЯєЄіІїЇёЁҐґ _-]{1,64}', name)
    return False

def currencySymbol(symbol):
    if isinstance(symbol, str):
        return re.fullmatch(r'.{1,8}', symbol)
    return False

#     ##     ##  ######  ######## ########
#     ##     ## ##    ## ##       ##     ##
#     ##     ## ##       ##       ##     ##
#     ##     ##  ######  ######   ########
#     ##     ##       ## ##       ##   ##
#     ##     ## ##    ## ##       ##    ##
#      #######   ######  ######## ##     ##

def userID(user_id):
    if isinstance(user_id, str):
        return bool(re.fullmatch(r'[0-9]{1,8}', user_id))
    if isinstance(user_id, int):
        return 1 <= len(str(user_id)) <= 8
    return False

def usersGroupID(users_group_id):
    if isinstance(users_group_id, str):
        return bool(re.fullmatch(r'[0-9]{1}', users_group_id))
    if isinstance(users_group_id, int):
        return len(str(users_group_id)) == 1
    return False

def userName(name):
    if isinstance(name, str):
        return re.fullmatch(r'\w{1,64}', name)
    return False

def usersGroupName(name):
    if isinstance(name, str):
        return re.fullmatch(r'\w{1,64}', name)
    return False

#      ######     ###    ######## ########  ######    #######  ########  ##    ##
#     ##    ##   ## ##      ##    ##       ##    ##  ##     ## ##     ##  ##  ##
#     ##        ##   ##     ##    ##       ##        ##     ## ##     ##   ####
#     ##       ##     ##    ##    ######   ##   #### ##     ## ########     ##
#     ##       #########    ##    ##       ##    ##  ##     ## ##   ##      ##
#     ##    ## ##     ##    ##    ##       ##    ##  ##     ## ##    ##     ##
#      ######  ##     ##    ##    ########  ######    #######  ##     ##    ##

def categoryID(category_id):
    if isinstance(category_id, str):
        return bool(re.fullmatch(r'[0-9]{1,8}', category_id))
    if isinstance(category_id, int):
        return 1 <= len(str(category_id)) <= 8
    return False

def categoryName(name):
    if isinstance(name, str):
        return re.fullmatch(r'\w{1,64}', name)
    return False

#     ########  ########   #######  ########  ##     ##  ######  ########  ######
#     ##     ## ##     ## ##     ## ##     ## ##     ## ##    ##    ##    ##    ##
#     ##     ## ##     ## ##     ## ##     ## ##     ## ##          ##    ##
#     ########  ########  ##     ## ##     ## ##     ## ##          ##     ######
#     ##        ##   ##   ##     ## ##     ## ##     ## ##          ##          ##
#     ##        ##    ##  ##     ## ##     ## ##     ## ##    ##    ##    ##    ##
#     ##        ##     ##  #######  ########   #######   ######     ##     ######

def productID(product_id):
    if isinstance(product_id, str):
        return bool(re.fullmatch(r'[0-9]{1,8}', product_id))
    if isinstance(product_id, int):
        return 1 <= len(str(product_id)) <= 8
    return False

def productModel(model):
    if isinstance(model, str):
        return re.fullmatch(r'[0-9A-Za-zА-Яа-яЯєЄіІїЇёЁҐґ _-]{1,64}', model)
    return False

def productName(name):
    if isinstance(name, str):
        return re.fullmatch(r'[0-9A-Za-zА-Яа-яЯєЄіІїЇёЁҐґ _-]{1,128}', name)
    return False

def productDescrioption(description):
    if isinstance(description, str):
        return re.fullmatch(r'[0-9A-Za-zА-Яа-яЯєЄіІїЇёЁҐґ _-]{1,256}', description)
    return False

#      ######  ##     ##    ###    ########     ###     ######  ######## ######## ########  ####  ######  ######## ####  ######
#     ##    ## ##     ##   ## ##   ##     ##   ## ##   ##    ##    ##    ##       ##     ##  ##  ##    ##    ##     ##  ##    ##
#     ##       ##     ##  ##   ##  ##     ##  ##   ##  ##          ##    ##       ##     ##  ##  ##          ##     ##  ##
#     ##       ######### ##     ## ########  ##     ## ##          ##    ######   ########   ##   ######     ##     ##  ##
#     ##       ##     ## ######### ##   ##   ######### ##          ##    ##       ##   ##    ##        ##    ##     ##  ##
#     ##    ## ##     ## ##     ## ##    ##  ##     ## ##    ##    ##    ##       ##    ##   ##  ##    ##    ##     ##  ##    ##
#      ######  ##     ## ##     ## ##     ## ##     ##  ######     ##    ######## ##     ## ####  ######     ##    ####  ######

def characteristicID(characteristic_id):
    if isinstance(characteristic_id, str):
        return bool(re.fullmatch(r'[0-9]{1,8}', characteristic_id))
    if isinstance(characteristic_id, int):
        return 1 <= len(str(characteristic_id)) <= 8
    return False

def characteristicName(name):
    if isinstance(name, str):
        return re.fullmatch(r'[0-9A-Za-zА-Яа-яЯєЄіІїЇёЁҐґ _-]{1,32}', name)
    return False
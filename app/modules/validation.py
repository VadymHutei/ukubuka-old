import re

def menuItemID(item_id):
    if isinstance(item_id, str):
        return bool(re.fullmatch(r'\d{1,4}', item_id))
    return False

def userID(user_id):
    if isinstance(user_id, str):
        return bool(re.fullmatch(r'\d{1,8}', user_id))
    return False

def usersGroupID(users_group_id):
    if isinstance(users_group_id, str):
        return bool(re.fullmatch(r'\d{1}', users_group_id))
    return False

def menuName(name):
    if isinstance(name, str):
        return name == '' or re.fullmatch(r'\w{1,32}', name)
    return False

def menuItemName(name):
    if isinstance(name, str):
        return name == '' or re.fullmatch(r'\w{1,64}', name)
    return False

def userName(name):
    if isinstance(name, str):
        return name == '' or re.fullmatch(r'\w{1,64}', name)
    return False

def phoneNumber(phone_number):
    if isinstance(phone_number, str):
        return phone_number == '' or re.fullmatch(r'[0-9+() -]{9,64}', phone_number)
    return False

def email(email):
    if isinstance(email, str):
        return email == '' or re.fullmatch(r'[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+', email)
    return False

def usersGroupName(name):
    if isinstance(name, str):
        return name == '' or re.fullmatch(r'\w{1,64}', name)
    return False

def menuItemLink(link):
    if isinstance(link, str):
        return bool(re.fullmatch(r'[\w:./]{1,128}', link))
    return False

def settingsProperty(prop):
    if isinstance(prop, str):
        return prop == '' or re.fullmatch(r'[\w. -]{1,64}', prop)
    return False

def password(prop):
    if isinstance(prop, str):
        return prop == '' or re.fullmatch(r'[\w\W]{3,64}', prop)
    return False

def sessionId(session_id):
    if isinstance(session_id, str):
        return bool(re.fullmatch(r'[0-9a-z]{64}', session_id))
    return False
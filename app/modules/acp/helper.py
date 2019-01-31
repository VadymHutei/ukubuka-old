import re



#     ##     ##    ###    ##       #### ########     ###    ######## ####  #######  ##    ##
#     ##     ##   ## ##   ##        ##  ##     ##   ## ##      ##     ##  ##     ## ###   ##
#     ##     ##  ##   ##  ##        ##  ##     ##  ##   ##     ##     ##  ##     ## ####  ##
#     ##     ## ##     ## ##        ##  ##     ## ##     ##    ##     ##  ##     ## ## ## ##
#      ##   ##  ######### ##        ##  ##     ## #########    ##     ##  ##     ## ##  ####
#       ## ##   ##     ## ##        ##  ##     ## ##     ##    ##     ##  ##     ## ##   ###
#        ###    ##     ## ######## #### ########  ##     ##    ##    ####  #######  ##    ##

def validMenuItemID(item_id):
    if isinstance(item_id, str):
        return bool(re.fullmatch(r'\d{1,4}', item_id))
    return False

def validUserID(user_id):
    if isinstance(user_id, str):
        return bool(re.fullmatch(r'\d{1,8}', user_id))
    return False

def validUsersGroupID(users_group_id):
    if isinstance(users_group_id, str):
        return bool(re.fullmatch(r'\d{1}', users_group_id))
    return False

def validMenuName(name):
    if isinstance(name, str):
        return name == '' or re.fullmatch(r'\w{1,32}', name)
    return False

def validMenuItemName(name):
    if isinstance(name, str):
        return name == '' or re.fullmatch(r'\w{1,64}', name)
    return False

def validUserName(name):
    if isinstance(name, str):
        return name == '' or re.fullmatch(r'\w{1,64}', name)
    return False

def validPhoneNumber(phone_number):
    if isinstance(phone_number, str):
        return phone_number == '' or re.fullmatch(r'[0-9+() -]{7,64}', phone_number)
    return False

def validEmail(email):
    if isinstance(email, str):
        return email == '' or re.fullmatch(r'[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+', email)
    return False

def validUsersGroupName(name):
    if isinstance(name, str):
        return name == '' or re.fullmatch(r'\w{1,64}', name)
    return False

def validMenuItemLink(link):
    if isinstance(link, str):
        return bool(re.fullmatch(r'[\w:./]{1,128}', link))
    return False



#     ##     ## ######## ##    ## ##     ##
#     ###   ### ##       ###   ## ##     ##
#     #### #### ##       ####  ## ##     ##
#     ## ### ## ######   ## ## ## ##     ##
#     ##     ## ##       ##  #### ##     ##
#     ##     ## ##       ##   ### ##     ##
#     ##     ## ######## ##    ##  #######

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



#     ##     ##  ######  ######## ########   ######
#     ##     ## ##    ## ##       ##     ## ##    ##
#     ##     ## ##       ##       ##     ## ##
#     ##     ##  ######  ######   ########   ######
#     ##     ##       ## ##       ##   ##         ##
#     ##     ## ##    ## ##       ##    ##  ##    ##
#      #######   ######  ######## ##     ##  ######

def prepareUserFormData(form):
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
    result = {}
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
    return result

def validAddUserData(data):
    if 'group_id' not in data or not validUsersGroupID(data['group_id']): return False
    if 'is_active' not in data or data['is_active'] not in ['Y', 'N']: return False
    if 'first_name' in data and not validUserName(data['first_name']): return False
    if 'patronymic' in data and not validUserName(data['patronymic']): return False
    if 'last_name' in data and not validUserName(data['last_name']): return False
    if 'phone_number' in data and not validPhoneNumber(data['phone_number']): return False
    if 'email' in data and not validEmail(data['email']): return False
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
    return result

def validEditUserData(data):
    if 'user_id' not in data or not validUserID(data['user_id']): return False
    if 'group_id' in data and not validUsersGroupID(data['group_id']): return False
    if 'is_active' in data and data['is_active'] not in ['Y', 'N']: return False
    if 'first_name' in data and not validUserName(data['first_name']): return False
    if 'patronymic' in data and not validUserName(data['patronymic']): return False
    if 'last_name' in data and not validUserName(data['last_name']): return False
    if 'phone_number' in data and not validPhoneNumber(data['phone_number']): return False
    if 'phone_numbers' in data:
        for phone_number in data['phone_numbers']:
            if not validPhoneNumber(phone_number): return False
    if 'email' in data and not validEmail(data['email']): return False
    if 'emails' in data:
        for email in data['emails']:
            if not validEmail(email): return False
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
    return result



#     ##     ##  ######  ######## ########   ######      ######   ########   #######  ##     ## ########   ######
#     ##     ## ##    ## ##       ##     ## ##    ##    ##    ##  ##     ## ##     ## ##     ## ##     ## ##    ##
#     ##     ## ##       ##       ##     ## ##          ##        ##     ## ##     ## ##     ## ##     ## ##
#     ##     ##  ######  ######   ########   ######     ##   #### ########  ##     ## ##     ## ########   ######
#     ##     ##       ## ##       ##   ##         ##    ##    ##  ##   ##   ##     ## ##     ## ##              ##
#     ##     ## ##    ## ##       ##    ##  ##    ##    ##    ##  ##    ##  ##     ## ##     ## ##        ##    ##
#      #######   ######  ######## ##     ##  ######      ######   ##     ##  #######   #######  ##         ######

def prepareUsersGroupFormData(form):
    group_id = form.get('id')
    name = form.get('name')
    result = {}
    if group_id: result['group_id'] = group_id
    if name: result['name'] = name
    return result

def validAddUsersGroupData(data):
    if 'name' not in data or not validUsersGroupName(data['name']): return False
    return True

def prepareAddUsersGroupData(data):
    result = {'name': data['name']}
    return result

def validEditUsersGroupData(data):
    if 'group_id' not in data or not validUsersGroupID(data['group_id']): return False
    if 'name' not in data or not validUsersGroupName(data['name']): return False
    return True

def prepareEditUsersGroupData(data):
    result = {
        'group_id': data['group_id'],
        'name': data['name']
    }
    return result
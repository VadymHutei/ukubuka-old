import config
import modules.lib.validation as validation
import modules.lib.auth as auth



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
    if 'menu' not in data or not validation.menuName(data['menu']): return False
    if 'name_ukr' not in data or not validation.menuItemName(data['name_ukr']): return False
    if 'name_eng' not in data or not validation.menuItemName(data['name_eng']): return False
    if 'link' in data and not validation.menuItemLink(data['link']): return False
    if 'parent' in data and not validation.menuItemID(data['parent']): return False
    if 'is_active' in data and data['is_active'] not in ['Y', 'N']: return False
    return True

def validEditMenuItemData(data):
    if 'item_id' not in data or not validation.menuItemID(data['item_id']): return False
    if 'menu' in data and not validation.menuName(data['menu']): return False
    if 'name_ukr' in data and not validation.menuItemName(data['name_ukr']): return False
    if 'name_eng' in data and not validation.menuItemName(data['name_eng']): return False
    if 'link' in data and not validation.menuItemLink(data['link']): return False
    if 'parent' in data and not validation.menuItemID(data['parent']): return False
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
    password = form.get('password')
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
    if password: result['password'] = password
    return result

def validAddUserData(data):
    if 'group_id' not in data or not validation.usersGroupID(data['group_id']): return False
    if 'is_active' not in data or data['is_active'] not in ['Y', 'N']: return False
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
        salt = generateSalt()
        result['salt'] = salt
        result['password'] = hashPassword(data['password'], salt)
    return result

def validEditUserData(data):
    if 'user_id' not in data or not validation.userID(data['user_id']): return False
    if 'group_id' in data and not validation.usersGroupID(data['group_id']): return False
    if 'is_active' in data and data['is_active'] not in ['Y', 'N']: return False
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
    if 'name' not in data or not validation.usersGroupName(data['name']): return False
    return True

def prepareAddUsersGroupData(data):
    result = {'name': data['name']}
    return result

def validEditUsersGroupData(data):
    if 'group_id' not in data or not validation.usersGroupID(data['group_id']): return False
    if 'name' not in data or not validation.usersGroupName(data['name']): return False
    return True

def prepareEditUsersGroupData(data):
    result = {
        'group_id': data['group_id'],
        'name': data['name']
    }
    return result



#      ######  ######## ######## ######## #### ##    ##  ######    ######
#     ##    ## ##          ##       ##     ##  ###   ## ##    ##  ##    ##
#     ##       ##          ##       ##     ##  ####  ## ##        ##
#      ######  ######      ##       ##     ##  ## ## ## ##   ####  ######
#           ## ##          ##       ##     ##  ##  #### ##    ##        ##
#     ##    ## ##          ##       ##     ##  ##   ### ##    ##  ##    ##
#      ######  ########    ##       ##    #### ##    ##  ######    ######



def validSaveSettingsData(data):
    for prop in data:
        if not validation.settingsProperty(data[prop]): return False
    return True

def prepareSaveSettingsData(settings, data):
    result = {}
    for prop in data:
        if prop not in settings: continue
        if data[prop] == settings[prop]: continue
        result[prop] = data[prop]
    return result
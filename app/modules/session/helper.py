import random
import config
import modules.lib.validation as validation



#      ######  ########  ######   ######  ####  #######  ##    ##
#     ##    ## ##       ##    ## ##    ##  ##  ##     ## ###   ##
#     ##       ##       ##       ##        ##  ##     ## ####  ##
#      ######  ######    ######   ######   ##  ##     ## ## ## ##
#           ## ##             ##       ##  ##  ##     ## ##  ####
#     ##    ## ##       ##    ## ##    ##  ##  ##     ## ##   ###
#      ######  ########  ######   ######  ####  #######  ##    ##



def create_session_id():
    return ''.join([random.choice(config.session_id_available_characters) for _ in range(64)])



#        ###    ##     ## ######## ##     ## ######## ##    ## ######## ####  ######     ###    ######## ####  #######  ##    ##
#       ## ##   ##     ##    ##    ##     ## ##       ###   ##    ##     ##  ##    ##   ## ##      ##     ##  ##     ## ###   ##
#      ##   ##  ##     ##    ##    ##     ## ##       ####  ##    ##     ##  ##        ##   ##     ##     ##  ##     ## ####  ##
#     ##     ## ##     ##    ##    ######### ######   ## ## ##    ##     ##  ##       ##     ##    ##     ##  ##     ## ## ## ##
#     ######### ##     ##    ##    ##     ## ##       ##  ####    ##     ##  ##       #########    ##     ##  ##     ## ##  ####
#     ##     ## ##     ##    ##    ##     ## ##       ##   ###    ##     ##  ##    ## ##     ##    ##     ##  ##     ## ##   ###
#     ##     ##  #######     ##    ##     ## ######## ##    ##    ##    ####  ######  ##     ##    ##    ####  #######  ##    ##



def prepareAuthenticationFormData(form):
    result = {}
    email = form.get('email')
    password = form.get('password')
    if email: result['email'] = email
    if password: result['password'] = password
    return result

def validAuthenticationData(data):
    if 'email' not in data or not validation.email(data['email']): return False
    if 'password' not in data or not validation.password(data['password']): return False
    return True
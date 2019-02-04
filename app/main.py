import datetime
from flask import Flask, request, redirect, url_for, abort, render_template, after_this_request
from functools import wraps
import config
from modules.session.ctrl import Session
from modules.main.ctrl import Main
from modules.acp.ctrl import Acp
from modules.test.ctrl import Test

def lang_redirect(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'lang' in kwargs:
            if kwargs['lang'] == config.default_language:
                return redirect(url_for(f.__name__))
            if kwargs['lang'] not in config.languages:
                return redirect(url_for(f.__name__))
        return f(*args, **kwargs)
    return decorated_function

def admin_access(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if True:
            return redirect(url_for('acp_authorization'), 403)
        return f(*args, **kwargs)
    return decorated_function

app = Flask(__name__)

@app.before_request
def start_session():
    session = Session(request.cookies.get(config.session_cookie_name), remote_address=request.remote_addr)
    if not session.isValid():
        session_id = session.start()
        if not session_id: return
        @after_this_request
        def set_session_cookie(response):
            expire_date = datetime.datetime.now() + datetime.timedelta(days=config.session_cookie_expires)
            response.set_cookie(config.session_cookie_name, session_id, expires=expire_date, path='/')
            return response
    session.increaseVisits()



#     ##     ##    ###    #### ##    ##
#     ###   ###   ## ##    ##  ###   ##
#     #### ####  ##   ##   ##  ####  ##
#     ## ### ## ##     ##  ##  ## ## ##
#     ##     ## #########  ##  ##  ####
#     ##     ## ##     ##  ##  ##   ###
#     ##     ## ##     ## #### ##    ##



@app.route('/', methods=['GET'])
def main():
    mod = Main()
    return mod.main_page()



#     ######## ########  ######  ########
#        ##    ##       ##    ##    ##
#        ##    ##       ##          ##
#        ##    ######    ######     ##
#        ##    ##             ##    ##
#        ##    ##       ##    ##    ##
#        ##    ########  ######     ##



@app.route('/test')
def test():
    mod = Test()
    return mod.test()



#
#
#            _         ____   ________
#           dM.       6MMMMb/ `MMMMMMMb.
#          ,MMb      8P    YM  MM    `Mb
#          d'YM.    6M      Y  MM     MM
#         ,P `Mb    MM         MM     MM
#         d'  YM.   MM         MM    .M9
#        ,P   `Mb   MM         MMMMMMM9'
#        d'    YM.  MM         MM
#       ,MMMMMMMMb  YM      6  MM
#       d'      YM.  8b    d9  MM
#     _dM_     _dMM_  YMMMM9  _MM_
#
#
#



@app.route('/acp', methods=['GET'])
@app.route('/<lang>/acp', methods=['GET'])
@admin_access
@lang_redirect
def acp(lang=config.default_language):
    return redirect(url_for('acp_dashboard', lang=lang), 302)

@app.route('/acp/authorization', methods=['GET'])
@app.route('/<lang>/acp/authorization', methods=['GET'])
@lang_redirect
def acp_authorization(lang=config.default_language):
    mod = Acp(lang)
    return mod.authorization_page()



#     ########     ###     ######  ##     ## ########   #######     ###    ########  ########
#     ##     ##   ## ##   ##    ## ##     ## ##     ## ##     ##   ## ##   ##     ## ##     ##
#     ##     ##  ##   ##  ##       ##     ## ##     ## ##     ##  ##   ##  ##     ## ##     ##
#     ##     ## ##     ##  ######  ######### ########  ##     ## ##     ## ########  ##     ##
#     ##     ## #########       ## ##     ## ##     ## ##     ## ######### ##   ##   ##     ##
#     ##     ## ##     ## ##    ## ##     ## ##     ## ##     ## ##     ## ##    ##  ##     ##
#     ########  ##     ##  ######  ##     ## ########   #######  ##     ## ##     ## ########



@app.route('/acp/dashboard', methods=['GET'])
@app.route('/<lang>/acp/dashboard', methods=['GET'])
@admin_access
@lang_redirect
def acp_dashboard(lang=config.default_language):
    mod = Acp(lang)
    return mod.dashboard_page()



#     ##     ##  ######  ######## ########   ######
#     ##     ## ##    ## ##       ##     ## ##    ##
#     ##     ## ##       ##       ##     ## ##
#     ##     ##  ######  ######   ########   ######
#     ##     ##       ## ##       ##   ##         ##
#     ##     ## ##    ## ##       ##    ##  ##    ##
#      #######   ######  ######## ##     ##  ######



@app.route('/acp/users/', methods=['GET'])
@app.route('/<lang>/acp/users/', methods=['GET'])
@admin_access
@lang_redirect
def acp_users(lang=config.default_language):
    mod = Acp(lang)
    return mod.users_page()

@app.route('/acp/users/add', methods=['GET', 'POST'])
@app.route('/<lang>/acp/users/add', methods=['GET', 'POST'])
@admin_access
@lang_redirect
def acp_users_add(lang=config.default_language):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.user_add_page()
    else:
        mod.addUser(request.form)
        return redirect(url_for('acp_users'), 303)

@app.route('/acp/users/edit', methods=['GET', 'POST'])
@app.route('/<lang>/acp/users/edit', methods=['GET', 'POST'])
@admin_access
@lang_redirect
def acp_users_edit(lang=config.default_language):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.user_edit_page(request.args['id'])
    else:
        mod.editUser(request.form)
        return redirect(url_for('acp_users'), 303)

@app.route('/acp/users/delete', methods=['GET'])
@app.route('/<lang>/acp/users/delete', methods=['GET'])
@admin_access
@lang_redirect
def acp_users_delete(lang=config.default_language):
    mod = Acp(lang)
    mod.deleteUser(request.args['id'])
    return redirect(url_for('acp_users'), 303)

@app.route('/acp/users/add_phone_number', methods=['GET', 'POST'])
@app.route('/<lang>/acp/users/add_phone_number', methods=['GET', 'POST'])
@admin_access
@lang_redirect
def acp_users_add_phone_number(lang=config.default_language):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.user_add_phone_number_page(request.args['id'])
    else:
        mod.addUserPhoneNumber(request.form)
        return redirect(url_for('acp_users'), 303)

@app.route('/acp/users/add_email', methods=['GET', 'POST'])
@app.route('/<lang>/acp/users/add_email', methods=['GET', 'POST'])
@admin_access
@lang_redirect
def acp_users_add_email(lang=config.default_language):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.user_add_email_page(request.args['id'])
    else:
        mod.addUserEmail(request.form)
        return redirect(url_for('acp_users'), 303)



#     ##     ##  ######  ######## ########   ######      ######   ########   #######  ##     ## ########   ######
#     ##     ## ##    ## ##       ##     ## ##    ##    ##    ##  ##     ## ##     ## ##     ## ##     ## ##    ##
#     ##     ## ##       ##       ##     ## ##          ##        ##     ## ##     ## ##     ## ##     ## ##
#     ##     ##  ######  ######   ########   ######     ##   #### ########  ##     ## ##     ## ########   ######
#     ##     ##       ## ##       ##   ##         ##    ##    ##  ##   ##   ##     ## ##     ## ##              ##
#     ##     ## ##    ## ##       ##    ##  ##    ##    ##    ##  ##    ##  ##     ## ##     ## ##        ##    ##
#      #######   ######  ######## ##     ##  ######      ######   ##     ##  #######   #######  ##         ######



@app.route('/acp/users/groups/', methods=['GET'])
@app.route('/<lang>/acp/users/groups/', methods=['GET'])
@admin_access
@lang_redirect
def acp_users_groups(lang=config.default_language):
    mod = Acp(lang)
    return mod.users_groups_page()

@app.route('/acp/users/groups/add', methods=['GET', 'POST'])
@app.route('/<lang>/acp/users/groups/add', methods=['GET', 'POST'])
@admin_access
@lang_redirect
def acp_users_groups_add(lang=config.default_language):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.users_groups_add_page()
    else:
        mod.addUsersGroup(request.form)
        return redirect(url_for('acp_users_groups'), 303)

@app.route('/acp/users/groups/edit', methods=['GET', 'POST'])
@app.route('/<lang>/acp/users/groups/edit', methods=['GET', 'POST'])
@admin_access
@lang_redirect
def acp_users_groups_edit(lang=config.default_language):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.users_groups_edit_page(request.args['id'])
    else:
        mod.editUsersGroup(request.form)
        return redirect(url_for('acp_users_groups'), 303)

@app.route('/acp/users/groups/delete', methods=['GET'])
@app.route('/<lang>/acp/users/groups/delete', methods=['GET'])
@admin_access
@lang_redirect
def acp_users_groups_delete(lang=config.default_language):
    mod = Acp(lang)
    mod.deleteUsersGroup(request.args['id'])
    return redirect(url_for('acp_users_groups'), 303)



#     ##     ## ######## ##    ## ##     ##  ######
#     ###   ### ##       ###   ## ##     ## ##    ##
#     #### #### ##       ####  ## ##     ## ##
#     ## ### ## ######   ## ## ## ##     ##  ######
#     ##     ## ##       ##  #### ##     ##       ##
#     ##     ## ##       ##   ### ##     ## ##    ##
#     ##     ## ######## ##    ##  #######   ######



@app.route('/acp/menus/', methods=['GET'])
@app.route('/<lang>/acp/menus/', methods=['GET'])
@admin_access
@lang_redirect
def acp_menus(lang=config.default_language):
    mod = Acp(lang)
    return mod.menus_page()

@app.route('/acp/menus/add', methods=['GET', 'POST'])
@app.route('/<lang>/acp/menus/add', methods=['GET', 'POST'])
@admin_access
@lang_redirect
def acp_menus_add(lang=config.default_language):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.menus_add_page()
    else:
        mod.addMenuItem(request.form)
        return redirect(url_for('acp_menus'), 303)

@app.route('/acp/menus/edit', methods=['GET', 'POST'])
@app.route('/<lang>/acp/menus/edit', methods=['GET', 'POST'])
@admin_access
@lang_redirect
def acp_menus_edit(lang=config.default_language):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.menus_edit_page(request.args['id'])
    else:
        mod.editMenuItem(request.form)
        return redirect(url_for('acp_menus'), 303)

@app.route('/acp/menus/delete', methods=['GET'])
@app.route('/<lang>/acp/menus/delete', methods=['GET'])
@admin_access
@lang_redirect
def acp_menus_delete(lang=config.default_language):
    mod = Acp(lang)
    mod.deleteMenuItem(request.args['id'])
    return redirect(url_for('acp_menus'), 303)



#      ######  ######## ######## ######## #### ##    ##  ######    ######
#     ##    ## ##          ##       ##     ##  ###   ## ##    ##  ##    ##
#     ##       ##          ##       ##     ##  ####  ## ##        ##
#      ######  ######      ##       ##     ##  ## ## ## ##   ####  ######
#           ## ##          ##       ##     ##  ##  #### ##    ##        ##
#     ##    ## ##          ##       ##     ##  ##   ### ##    ##  ##    ##
#      ######  ########    ##       ##    #### ##    ##  ######    ######



@app.route('/acp/settings', methods=['GET', 'POST'])
@app.route('/<lang>/acp/settings', methods=['GET', 'POST'])
@admin_access
@lang_redirect
def acp_settings(lang=config.default_language):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.settings_page()
    else:
        mod.saveSettings(request.form)
        return redirect(url_for('acp_settings'), 303)



#
#
#     __________ ________    ________       ____    ________      ____
#     `MMMMMMMMM `MMMMMMMb.  `MMMMMMMb.    6MMMMb   `MMMMMMMb.   6MMMMb\
#      MM      \  MM    `Mb   MM    `Mb   8P    Y8   MM    `Mb  6M'    `
#      MM         MM     MM   MM     MM  6M      Mb  MM     MM  MM
#      MM    ,    MM     MM   MM     MM  MM      MM  MM     MM  YM.
#      MMMMMMM    MM    .M9   MM    .M9  MM      MM  MM    .M9   YMMMMb
#      MM    `    MMMMMMM9'   MMMMMMM9'  MM      MM  MMMMMMM9'       `Mb
#      MM         MM  \M\     MM  \M\    MM      MM  MM  \M\          MM
#      MM         MM   \M\    MM   \M\   YM      M9  MM   \M\         MM
#      MM      /  MM    \M\   MM    \M\   8b    d8   MM    \M\  L    ,M9
#     _MMMMMMMMM _MM_    \M\__MM_    \M\_  YMMMM9   _MM_    \M\_MYMMMM9
#
#
#



@app.errorhandler(400)
def page_not_found(error):
    return render_template('errors/400.html'), 400

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def page_not_found(error):
    return render_template('errors/500.html', error=error), 500

if __name__ == "__main__":
    app.run(**config.app_config)
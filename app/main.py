from flask import Flask, request, redirect, url_for, abort, render_template
from functools import wraps
import config
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

app = Flask(__name__)

#
#
#     ___       ___   ____    ________   ____     _______     __________   ____
#     `MMb     dMM'  6MMMMb   `MMMMMMMb. `MM'     `M'`MM'     `MMMMMMMMM  6MMMMb\
#      MMM.   ,PMM  8P    Y8   MM    `Mb  MM       M  MM       MM      \ 6M'    `
#      M`Mb   d'MM 6M      Mb  MM     MM  MM       M  MM       MM        MM
#      M YM. ,P MM MM      MM  MM     MM  MM       M  MM       MM    ,   YM.
#      M `Mb d' MM MM      MM  MM     MM  MM       M  MM       MMMMMMM    YMMMMb
#      M  YM.P  MM MM      MM  MM     MM  MM       M  MM       MM    `        `Mb
#      M  `Mb'  MM MM      MM  MM     MM  MM       M  MM       MM              MM
#      M   YP   MM YM      M9  MM     MM  YM       M  MM       MM              MM
#      M   `'   MM  8b    d8   MM    .M9   8b     d8  MM    /  MM      / L    ,M9
#     _M_      _MM_  YMMMM9   _MMMMMMM9'    YMMMMM9  _MMMMMMM _MMMMMMMMM MYMMMM9
#
#
#

#     ##     ##    ###    #### ##    ##
#     ###   ###   ## ##    ##  ###   ##
#     #### ####  ##   ##   ##  ####  ##
#     ## ### ## ##     ##  ##  ## ## ##
#     ##     ## #########  ##  ##  ####
#     ##     ## ##     ##  ##  ##   ###
#     ##     ## ##     ## #### ##    ##

@app.route('/')
def main():
    mod = Main()
    return mod.view

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

#     ########     ###     ######  ##     ## ########   #######     ###    ########  ########
#     ##     ##   ## ##   ##    ## ##     ## ##     ## ##     ##   ## ##   ##     ## ##     ##
#     ##     ##  ##   ##  ##       ##     ## ##     ## ##     ##  ##   ##  ##     ## ##     ##
#     ##     ## ##     ##  ######  ######### ########  ##     ## ##     ## ########  ##     ##
#     ##     ## #########       ## ##     ## ##     ## ##     ## ######### ##   ##   ##     ##
#     ##     ## ##     ## ##    ## ##     ## ##     ## ##     ## ##     ## ##    ##  ##     ##
#     ########  ##     ##  ######  ##     ## ########   #######  ##     ## ##     ## ########

@app.route('/acp', methods=['GET'])
def acp():
    lang = 'ukr'
    mod = Acp(lang)
    return mod.dashboard()

#     ##     ##  ######  ######## ########   ######
#     ##     ## ##    ## ##       ##     ## ##    ##
#     ##     ## ##       ##       ##     ## ##
#     ##     ##  ######  ######   ########   ######
#     ##     ##       ## ##       ##   ##         ##
#     ##     ## ##    ## ##       ##    ##  ##    ##
#      #######   ######  ######## ##     ##  ######

@app.route('/acp/users/', methods=['GET'])
def acp_users():
    lang = 'ukr'
    mod = Acp(lang)
    return mod.users()

@app.route('/acp/users/add', methods=['GET'])
def acp_users_add():
    lang = 'ukr'
    mod = Acp(lang)
    return mod.users_add()

@app.route('/acp/users/add', methods=['POST'])
def acp_users_add_post():
    lang = 'ukr'
    mod = Acp(lang)
    return 'DONE!'

#     ##     ## ######## ##    ## ##     ##  ######
#     ###   ### ##       ###   ## ##     ## ##    ##
#     #### #### ##       ####  ## ##     ## ##
#     ## ### ## ######   ## ## ## ##     ##  ######
#     ##     ## ##       ##  #### ##     ##       ##
#     ##     ## ##       ##   ### ##     ## ##    ##
#     ##     ## ######## ##    ##  #######   ######

@app.route('/acp/menus/', methods=['GET'])
@app.route('/<lang>/acp/menus/', methods=['GET'])
@lang_redirect
def acp_menus(lang=config.default_language):
    mod = Acp(lang)
    return mod.menus_page()

@app.route('/acp/menus/add', methods=['GET', 'POST'])
@app.route('/<lang>/acp/menus/add', methods=['GET', 'POST'])
@lang_redirect
def acp_menus_add(lang=config.default_language):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.menus_add_page()
    else:
        mod.addMenuItem(request.form)
        return redirect(url_for('acp_menus'))

@app.route('/acp/menus/edit', methods=['GET', 'POST'])
@app.route('/<lang>/acp/menus/edit', methods=['GET', 'POST'])
@lang_redirect
def acp_menus_edit(lang=config.default_language):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.menus_edit_page(request.args['id'])
    else:
        mod.editMenuItem(request.form)
        return redirect(url_for('acp_menus'))



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
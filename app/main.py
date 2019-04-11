import datetime
from flask import Flask, request, redirect, url_for, abort, render_template, after_this_request
from functools import wraps
import config
from modules.session.ctrl import Session
from modules.main.ctrl import Main
from modules.acp.ctrl import Acp
from modules.test.ctrl import Test

def langRedirect(f):
    @wraps(f)
    def decoratedFunction(*args, **kwargs):
        if 'lang' in kwargs:
            if kwargs['lang'] == config.DEFAULT_LANGUAGE:
                return redirect(url_for(f.__name__))
            if kwargs['lang'] not in config.LANGUAGES:
                return redirect(url_for(f.__name__))
        return f(*args, **kwargs)
    return decoratedFunction

def adminAccess(f):
    @wraps(f)
    def decoratedFunction(*args, **kwargs):
        session = Session(
            request.cookies.get(config.SESSION_COOKIE_NAME),
            remote_address=request.remote_addr,
            uic=request.cookies.get(config.UIC_NAME)
        )
        if not session.authorization('admin'):
            return redirect(url_for('acpAuthentication'), 303)
        return f(*args, **kwargs)
    return decoratedFunction

app = Flask(__name__)

@app.before_request
def startSession():
    session = Session(
        request.cookies.get(config.SESSION_COOKIE_NAME),
        remote_address=request.remote_addr,
        request_url=request.path
    )
    if not session.isValid():
        session_id = session.start()
        if not session_id: return
        @after_this_request
        def setSessionCookie(response):
            expire_date = datetime.datetime.now() + datetime.timedelta(days=config.SESSION_COOKIE_EXPIRES)
            response.set_cookie(config.SESSION_COOKIE_NAME, session_id, expires=expire_date, path='/')
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
    return mod.mainPage()



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
@langRedirect
def acp(lang=config.DEFAULT_LANGUAGE):
    return redirect(url_for('acpDashboard', lang=lang), 302)

@app.route('/acp/authentication', methods=['GET', 'POST'])
@app.route('/<lang>/acp/authentication', methods=['GET', 'POST'])
@langRedirect
def acpAuthentication(lang=config.DEFAULT_LANGUAGE):
    if request.method == 'GET':
        mod = Acp(lang)
        return mod.authenticationPage()
    else:
        session = Session(request.cookies.get(config.SESSION_COOKIE_NAME), remote_address=request.remote_addr)
        uic, expires = session.authentication(request.form)
        if uic:
            @after_this_request
            def set_token(response):
                response.set_cookie(config.UIC_NAME, uic, expires=expires, path='/')
                return response
            return redirect(url_for('acpDashboard', lang=lang), 303)
        else:
            return redirect(url_for('acpAuthentication'), 303)



#     ########     ###     ######  ##     ## ########   #######     ###    ########  ########
#     ##     ##   ## ##   ##    ## ##     ## ##     ## ##     ##   ## ##   ##     ## ##     ##
#     ##     ##  ##   ##  ##       ##     ## ##     ## ##     ##  ##   ##  ##     ## ##     ##
#     ##     ## ##     ##  ######  ######### ########  ##     ## ##     ## ########  ##     ##
#     ##     ## #########       ## ##     ## ##     ## ##     ## ######### ##   ##   ##     ##
#     ##     ## ##     ## ##    ## ##     ## ##     ## ##     ## ##     ## ##    ##  ##     ##
#     ########  ##     ##  ######  ##     ## ########   #######  ##     ## ##     ## ########



@app.route('/acp/dashboard', methods=['GET'])
@app.route('/<lang>/acp/dashboard', methods=['GET'])
# @adminAccess
@langRedirect
def acpDashboard(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    return mod.dashboardPage()



#      ######     ###    ######## ########  ######    #######  ########  #### ########  ######
#     ##    ##   ## ##      ##    ##       ##    ##  ##     ## ##     ##  ##  ##       ##    ##
#     ##        ##   ##     ##    ##       ##        ##     ## ##     ##  ##  ##       ##
#     ##       ##     ##    ##    ######   ##   #### ##     ## ########   ##  ######    ######
#     ##       #########    ##    ##       ##    ##  ##     ## ##   ##    ##  ##             ##
#     ##    ## ##     ##    ##    ##       ##    ##  ##     ## ##    ##   ##  ##       ##    ##
#      ######  ##     ##    ##    ########  ######    #######  ##     ## #### ########  ######



@app.route('/acp/categories/', methods=['GET'])
@app.route('/<lang>/acp/categories/', methods=['GET'])
# @adminAccess
@langRedirect
def acpCategories(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    return mod.categoriesPage(request.args.get('parent'))

@app.route('/acp/categories/add', methods=['GET', 'POST'])
@app.route('/<lang>/acp/categories/add', methods=['GET', 'POST'])
# @adminAccess
@langRedirect
def acpAddCategory(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.addCategoryPage()
    else:
        mod.addCategory(request.form)
        return redirect(url_for('acpCategories'), 303)

@app.route('/acp/categories/edit', methods=['GET', 'POST'])
@app.route('/<lang>/acp/categories/edit', methods=['GET', 'POST'])
# @adminAccess
@langRedirect
def acpEditCategory(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.editCategoryPage(request.args['id'])
    else:
        mod.editCategory(request.form)
        return redirect(url_for('acpCategories'), 303)

@app.route('/acp/categories/delete', methods=['GET'])
@app.route('/<lang>/acp/categories/delete', methods=['GET'])
# @adminAccess
@langRedirect
def acpDeleteCategory(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    mod.deleteCategory(request.args['id'])
    return redirect(url_for('acpCategories'), 303)



#     ########  ########   #######  ########  ##     ##  ######  ########  ######
#     ##     ## ##     ## ##     ## ##     ## ##     ## ##    ##    ##    ##    ##
#     ##     ## ##     ## ##     ## ##     ## ##     ## ##          ##    ##
#     ########  ########  ##     ## ##     ## ##     ## ##          ##     ######
#     ##        ##   ##   ##     ## ##     ## ##     ## ##          ##          ##
#     ##        ##    ##  ##     ## ##     ## ##     ## ##    ##    ##    ##    ##
#     ##        ##     ##  #######  ########   #######   ######     ##     ######



@app.route('/acp/products/', methods=['GET'])
@app.route('/<lang>/acp/products/', methods=['GET'])
# @adminAccess
@langRedirect
def acpProducts(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    return mod.productsPage(request.args.get('category'))

@app.route('/acp/products/add', methods=['GET', 'POST'])
@app.route('/<lang>/acp/products/add', methods=['GET', 'POST'])
# @adminAccess
@langRedirect
def acpAddProduct(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.addProductPage()
    else:
        mod.addProduct(request.form)
        return redirect(url_for('acpProducts'), 303)

@app.route('/acp/products/edit', methods=['GET', 'POST'])
@app.route('/<lang>/acp/products/edit', methods=['GET', 'POST'])
# @adminAccess
@langRedirect
def acpEditProduct(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.editProductPage(request.args['id'])
    else:
        mod.editProduct(request.form)
        return redirect(url_for('acpProducts'), 303)

@app.route('/acp/products/delete', methods=['GET'])
@app.route('/<lang>/acp/products/delete', methods=['GET'])
# @adminAccess
@langRedirect
def acpDeleteProduct(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    mod.deleteProduct(request.args['id'])
    return redirect(url_for('acpProducts'), 303)



#      ######  ##     ##    ###    ########     ###     ######  ######## ######## ########  ####  ######  ######## ####  ######   ######
#     ##    ## ##     ##   ## ##   ##     ##   ## ##   ##    ##    ##    ##       ##     ##  ##  ##    ##    ##     ##  ##    ## ##    ##
#     ##       ##     ##  ##   ##  ##     ##  ##   ##  ##          ##    ##       ##     ##  ##  ##          ##     ##  ##       ##
#     ##       ######### ##     ## ########  ##     ## ##          ##    ######   ########   ##   ######     ##     ##  ##        ######
#     ##       ##     ## ######### ##   ##   ######### ##          ##    ##       ##   ##    ##        ##    ##     ##  ##             ##
#     ##    ## ##     ## ##     ## ##    ##  ##     ## ##    ##    ##    ##       ##    ##   ##  ##    ##    ##     ##  ##    ## ##    ##
#      ######  ##     ## ##     ## ##     ## ##     ##  ######     ##    ######## ##     ## ####  ######     ##    ####  ######   ######



@app.route('/acp/characteristics/', methods=['GET'])
@app.route('/<lang>/acp/characteristics/', methods=['GET'])
# @adminAccess
@langRedirect
def acpCharacteristics(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    return mod.characteristicsPage()

@app.route('/acp/characteristics/add', methods=['GET', 'POST'])
@app.route('/<lang>/acp/characteristics/add', methods=['GET', 'POST'])
# @adminAccess
@langRedirect
def acpAddCharacteristics(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.addCharacteristicPage()
    else:
        mod.addCharacteristic(request.form)
        return redirect(url_for('acpCharacteristics'), 303)

@app.route('/acp/characteristics/edit', methods=['GET', 'POST'])
@app.route('/<lang>/acp/characteristics/edit', methods=['GET', 'POST'])
# @adminAccess
@langRedirect
def acpEditCharacteristics(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.editCharacteristicPage(request.args['id'])
    else:
        mod.editCharacteristic(request.form)
        return redirect(url_for('acpCharacteristics'), 303)

@app.route('/acp/characteristics/delete', methods=['GET'])
@app.route('/<lang>/acp/characteristics/delete', methods=['GET'])
# @adminAccess
@langRedirect
def acpDeleteCharacteristic(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    mod.deleteCharacteristic(request.args['id'])
    return redirect(url_for('acpCharacteristics'), 303)



#     ##     ##  ######  ######## ########   ######
#     ##     ## ##    ## ##       ##     ## ##    ##
#     ##     ## ##       ##       ##     ## ##
#     ##     ##  ######  ######   ########   ######
#     ##     ##       ## ##       ##   ##         ##
#     ##     ## ##    ## ##       ##    ##  ##    ##
#      #######   ######  ######## ##     ##  ######



@app.route('/acp/users/', methods=['GET'])
@app.route('/<lang>/acp/users/', methods=['GET'])
# @adminAccess
@langRedirect
def acpUsers(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    return mod.users_page()

@app.route('/acp/users/add', methods=['GET', 'POST'])
@app.route('/<lang>/acp/users/add', methods=['GET', 'POST'])
# @adminAccess
@langRedirect
def acpUsers_add(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.user_add_page()
    else:
        mod.addUser(request.form)
        return redirect(url_for('acpUsers'), 303)

@app.route('/acp/users/edit', methods=['GET', 'POST'])
@app.route('/<lang>/acp/users/edit', methods=['GET', 'POST'])
# @adminAccess
@langRedirect
def acpUsers_edit(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.user_edit_page(request.args['id'])
    else:
        mod.editUser(request.form)
        return redirect(url_for('acpUsers'), 303)

@app.route('/acp/users/delete', methods=['GET'])
@app.route('/<lang>/acp/users/delete', methods=['GET'])
# @adminAccess
@langRedirect
def acpUsers_delete(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    mod.deleteUser(request.args['id'])
    return redirect(url_for('acpUsers'), 303)

@app.route('/acp/users/add_phone_number', methods=['GET', 'POST'])
@app.route('/<lang>/acp/users/add_phone_number', methods=['GET', 'POST'])
# @adminAccess
@langRedirect
def acpUsers_add_phone_number(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.user_add_phone_number_page(request.args['id'])
    else:
        mod.addUserPhoneNumber(request.form)
        return redirect(url_for('acpUsers'), 303)

@app.route('/acp/users/add_email', methods=['GET', 'POST'])
@app.route('/<lang>/acp/users/add_email', methods=['GET', 'POST'])
# @adminAccess
@langRedirect
def acpUsers_add_email(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.user_add_email_page(request.args['id'])
    else:
        mod.addUserEmail(request.form)
        return redirect(url_for('acpUsers'), 303)



#     ##     ## ######## ##    ## ##     ##  ######
#     ###   ### ##       ###   ## ##     ## ##    ##
#     #### #### ##       ####  ## ##     ## ##
#     ## ### ## ######   ## ## ## ##     ##  ######
#     ##     ## ##       ##  #### ##     ##       ##
#     ##     ## ##       ##   ### ##     ## ##    ##
#     ##     ## ######## ##    ##  #######   ######



@app.route('/acp/menus/', methods=['GET'])
@app.route('/<lang>/acp/menus/', methods=['GET'])
# @adminAccess
@langRedirect
def acpMenus(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    return mod.menusPage()

@app.route('/acp/menus/add', methods=['GET', 'POST'])
@app.route('/<lang>/acp/menus/add', methods=['GET', 'POST'])
# @adminAccess
@langRedirect
def acpMenus_add(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.menusAddPage()
    else:
        mod.addMenuItem(request.form)
        return redirect(url_for('acpMenus'), 303)

@app.route('/acp/menus/edit', methods=['GET', 'POST'])
@app.route('/<lang>/acp/menus/edit', methods=['GET', 'POST'])
# @adminAccess
@langRedirect
def acpMenus_edit(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.menusEditPage(request.args['id'])
    else:
        mod.editMenuItem(request.form)
        return redirect(url_for('acpMenus'), 303)

@app.route('/acp/menus/delete', methods=['GET'])
@app.route('/<lang>/acp/menus/delete', methods=['GET'])
# @adminAccess
@langRedirect
def acpMenus_delete(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    mod.deleteMenuItem(request.args['id'])
    return redirect(url_for('acpMenus'), 303)



#      ######  ##     ## ########  ########  ######## ##    ##  ######  #### ########  ######
#     ##    ## ##     ## ##     ## ##     ## ##       ###   ## ##    ##  ##  ##       ##    ##
#     ##       ##     ## ##     ## ##     ## ##       ####  ## ##        ##  ##       ##
#     ##       ##     ## ########  ########  ######   ## ## ## ##        ##  ######    ######
#     ##       ##     ## ##   ##   ##   ##   ##       ##  #### ##        ##  ##             ##
#     ##    ## ##     ## ##    ##  ##    ##  ##       ##   ### ##    ##  ##  ##       ##    ##
#      ######   #######  ##     ## ##     ## ######## ##    ##  ######  #### ########  ######



@app.route('/acp/currencies/', methods=['GET'])
@app.route('/<lang>/acp/currencies/', methods=['GET'])
# @adminAccess
@langRedirect
def acpCurrencies(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    return mod.currenciesPage()

@app.route('/acp/currencies/add', methods=['GET', 'POST'])
@app.route('/<lang>/acp/currencies/add', methods=['GET', 'POST'])
# @adminAccess
@langRedirect
def acpCurrencies_add(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.currenciesAddPage()
    else:
        mod.addCurrency(request.form)
        return redirect(url_for('acpCurrencies'), 303)

@app.route('/acp/currencies/edit', methods=['GET', 'POST'])
@app.route('/<lang>/acp/currencies/edit', methods=['GET', 'POST'])
# @adminAccess
@langRedirect
def acpCurrencies_edit(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.currenciesEditPage(request.args['code'])
    else:
        mod.editCurrency(request.form)
        return redirect(url_for('acpCurrencies'), 303)

@app.route('/acp/currencies/delete', methods=['GET'])
@app.route('/<lang>/acp/currencies/delete', methods=['GET'])
# @adminAccess
@langRedirect
def acpCurrencies_delete(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    mod.deleteCurrency(request.args['code'])
    return redirect(url_for('acpCurrencies'), 303)



#     ##          ###    ##    ##  ######   ##     ##    ###     ######   ########  ######
#     ##         ## ##   ###   ## ##    ##  ##     ##   ## ##   ##    ##  ##       ##    ##
#     ##        ##   ##  ####  ## ##        ##     ##  ##   ##  ##        ##       ##
#     ##       ##     ## ## ## ## ##   #### ##     ## ##     ## ##   #### ######    ######
#     ##       ######### ##  #### ##    ##  ##     ## ######### ##    ##  ##             ##
#     ##       ##     ## ##   ### ##    ##  ##     ## ##     ## ##    ##  ##       ##    ##
#     ######## ##     ## ##    ##  ######    #######  ##     ##  ######   ########  ######



@app.route('/acp/languages/', methods=['GET'])
@app.route('/<lang>/acp/languages/', methods=['GET'])
# @adminAccess
@langRedirect
def acpLanguages(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    return mod.languagesPage()

@app.route('/acp/languages/add', methods=['GET', 'POST'])
@app.route('/<lang>/acp/languages/add', methods=['GET', 'POST'])
# @adminAccess
@langRedirect
def acpLanguages_add(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.languagesAddPage()
    else:
        mod.addLanguage(request.form)
        return redirect(url_for('acpLanguages'), 303)

@app.route('/acp/languages/edit', methods=['GET', 'POST'])
@app.route('/<lang>/acp/languages/edit', methods=['GET', 'POST'])
# @adminAccess
@langRedirect
def acpLanguages_edit(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    if request.method == 'GET':
        return mod.languagesEditPage(request.args['code'])
    else:
        mod.editLanguage(request.form)
        return redirect(url_for('acpLanguages'), 303)

@app.route('/acp/languages/delete', methods=['GET'])
@app.route('/<lang>/acp/languages/delete', methods=['GET'])
# @adminAccess
@langRedirect
def acpLanguages_delete(lang=config.DEFAULT_LANGUAGE):
    mod = Acp(lang)
    mod.deleteLanguage(request.args['code'])
    return redirect(url_for('acpLanguages'), 303)



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
    app.run(**config.APP_CONFIG)
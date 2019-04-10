from flask import render_template, abort
import config
import modules.acp.model as model
import modules.acp.helper as helper
import modules.validation as validation

class Acp():

    def __init__(self, lang=config.DEFAULT_LANGUAGE):
        self.current_language = lang if lang in config.LANGUAGES else config.DEFAULT_LANGUAGE
        layout_menus, layout_menus_order = model.getMenusTree(self.current_language, order_by='order', order_type='desc')
        self.data = {
            'layout_menus': layout_menus,
            'layout_menus_order': layout_menus_order,
            'site_name': config.SITE_NAME
        }



#        ###    ##     ## ######## ##     ## ######## ##    ## ######## ####  ######     ###    ######## ####  #######  ##    ##
#       ## ##   ##     ##    ##    ##     ## ##       ###   ##    ##     ##  ##    ##   ## ##      ##     ##  ##     ## ###   ##
#      ##   ##  ##     ##    ##    ##     ## ##       ####  ##    ##     ##  ##        ##   ##     ##     ##  ##     ## ####  ##
#     ##     ## ##     ##    ##    ######### ######   ## ## ##    ##     ##  ##       ##     ##    ##     ##  ##     ## ## ## ##
#     ######### ##     ##    ##    ##     ## ##       ##  ####    ##     ##  ##       #########    ##     ##  ##     ## ##  ####
#     ##     ## ##     ##    ##    ##     ## ##       ##   ###    ##     ##  ##    ## ##     ##    ##     ##  ##     ## ##   ###
#     ##     ##  #######     ##    ##     ## ######## ##    ##    ##    ####  ######  ##     ##    ##    ####  #######  ##    ##



    def authenticationPage(self):
        return render_template('acp/authentication.html', **self.data)



#     ########     ###     ######  ##     ## ########   #######     ###    ########  ########
#     ##     ##   ## ##   ##    ## ##     ## ##     ## ##     ##   ## ##   ##     ## ##     ##
#     ##     ##  ##   ##  ##       ##     ## ##     ## ##     ##  ##   ##  ##     ## ##     ##
#     ##     ## ##     ##  ######  ######### ########  ##     ## ##     ## ########  ##     ##
#     ##     ## #########       ## ##     ## ##     ## ##     ## ######### ##   ##   ##     ##
#     ##     ## ##     ## ##    ## ##     ## ##     ## ##     ## ##     ## ##    ##  ##     ##
#     ########  ##     ##  ######  ##     ## ########   #######  ##     ## ##     ## ########



    def dashboardPage(self):
        return render_template('acp/dashboard.html', **self.data)



#      ######     ###    ######## ########  ######    #######  ########  #### ########  ######
#     ##    ##   ## ##      ##    ##       ##    ##  ##     ## ##     ##  ##  ##       ##    ##
#     ##        ##   ##     ##    ##       ##        ##     ## ##     ##  ##  ##       ##
#     ##       ##     ##    ##    ######   ##   #### ##     ## ########   ##  ######    ######
#     ##       #########    ##    ##       ##    ##  ##     ## ##   ##    ##  ##             ##
#     ##    ## ##     ##    ##    ##       ##    ##  ##     ## ##    ##   ##  ##       ##    ##
#      ######  ##     ##    ##    ########  ######    #######  ##     ## #### ########  ######



    def categoriesPage(self, parent=None):
        if parent is None:
            categories, order = model.getCategories(self.current_language, order_by='order', order_type='desc')
        elif parent.isdecimal():
            parent = int(parent)
            if validation.categoryID(parent):
                categories, order = model.getCategories(self.current_language, parent=parent, order_by='order', order_type='desc')
                parent = model.getCategory(parent)
            else: return abort(404)
        else: return abort(404)
        self.data['categories'] = categories
        self.data['categories_order'] = order
        self.data['parent'] = parent
        self.data['category_names'] = model.getCategoryNames(self.current_language)
        return render_template('acp/categories/list.html', **self.data)

    def addCategoryPage(self):
        categories, order = model.getCategories(self.current_language, order_by='id', order_type='asc')
        self.data['categories'] = categories
        self.data['categories_order'] = order
        self.data['languages'] = config.LANGUAGES
        return render_template('acp/categories/add.html', **self.data)

    def addCategory(self, form):
        data = helper.prepareCategoryFormData(form)
        if helper.validAddCategoryData(data):
            data = helper.prepareAddCategoryData(data)
            model.addCategory(data)

    def editCategoryPage(self, category_id):
        if not validation.categoryID(category_id): return abort(404)
        category = model.getCategory(category_id)
        if not category: return abort(404)
        categories, order = model.getCategories(self.current_language, order_by='id', order_type='asc')
        self.data['categories'] = categories
        self.data['categories_order'] = order
        self.data['category'] = category
        self.data['languages'] = config.LANGUAGES
        return render_template('acp/categories/edit.html', **self.data)

    def editCategory(self, form):
        data = helper.prepareCategoryFormData(form)
        if helper.validEditCategoryData(data):
            data = helper.prepareEditCategoryData(data)
            model.editCategory(data)

    def deleteCategory(self, category_id):
        if validation.categoryID(category_id): return model.deleteCategory(category_id)
        return False



#     ########  ########   #######  ########  ##     ##  ######  ########  ######
#     ##     ## ##     ## ##     ## ##     ## ##     ## ##    ##    ##    ##    ##
#     ##     ## ##     ## ##     ## ##     ## ##     ## ##          ##    ##
#     ########  ########  ##     ## ##     ## ##     ## ##          ##     ######
#     ##        ##   ##   ##     ## ##     ## ##     ## ##          ##          ##
#     ##        ##    ##  ##     ## ##     ## ##     ## ##    ##    ##    ##    ##
#     ##        ##     ##  #######  ########   #######   ######     ##     ######



    def productsPage(self):
        self.data['products'] = model.getProducts(self.current_language)
        return render_template('acp/products/list.html', **self.data)

    def addProductPage(self):
        self.data['categories'] = model.getCategories(self.current_language)
        self.data['languages'] = config.LANGUAGES
        return render_template('acp/products/add.html', **self.data)

    def addProduct(self, form):
        data = helper.prepareProductFormData(form)
        if helper.validAddProductData(data):
            data = helper.prepareAddProductData(data)
            model.addProduct(data)



#      ######  ##     ##    ###    ########     ###     ######  ######## ######## ########  ####  ######  ######## ####  ######   ######
#     ##    ## ##     ##   ## ##   ##     ##   ## ##   ##    ##    ##    ##       ##     ##  ##  ##    ##    ##     ##  ##    ## ##    ##
#     ##       ##     ##  ##   ##  ##     ##  ##   ##  ##          ##    ##       ##     ##  ##  ##          ##     ##  ##       ##
#     ##       ######### ##     ## ########  ##     ## ##          ##    ######   ########   ##   ######     ##     ##  ##        ######
#     ##       ##     ## ######### ##   ##   ######### ##          ##    ##       ##   ##    ##        ##    ##     ##  ##             ##
#     ##    ## ##     ## ##     ## ##    ##  ##     ## ##    ##    ##    ##       ##    ##   ##  ##    ##    ##     ##  ##    ## ##    ##
#      ######  ##     ## ##     ## ##     ## ##     ##  ######     ##    ######## ##     ## ####  ######     ##    ####  ######   ######



    def characteristicsPage(self):
        self.data['characteristics'] = model.getCharacteristics(self.current_language)
        return render_template('acp/characteristics/list.html', **self.data)

    def addCharacteristicPage(self):
        self.data['languages'] = config.LANGUAGES
        return render_template('acp/characteristics/add.html', **self.data)

    def addCharacteristic(self, form):
        data = helper.prepareCharacteristicFormData(form)
        if helper.validAddCharacteristicData(data):
            data = helper.prepareAddCharacteristicData(data)
            model.addCharacteristic(data)

    def editCharacteristicPage(self, characteristic_id):
        self.data['characteristic'] = model.getCharacteristic(characteristic_id)
        if not self.data['characteristic']: return abort(404)
        self.data['languages'] = config.LANGUAGES
        return render_template('acp/characteristics/edit.html', **self.data)

    def editCharacteristic(self, form):
        data = helper.prepareCharacteristicFormData(form)
        if helper.validEditCharacteristicData(data):
            data = helper.prepareEditCharacteristicData(data)
            model.editCharacteristic(data)

    def deleteCharacteristic(self, characteristic_id):
        if validation.characteristicID(characteristic_id): return model.deleteCharacteristic(characteristic_id)



#     ##     ##  ######  ######## ########   ######
#     ##     ## ##    ## ##       ##     ## ##    ##
#     ##     ## ##       ##       ##     ## ##
#     ##     ##  ######  ######   ########   ######
#     ##     ##       ## ##       ##   ##         ##
#     ##     ## ##    ## ##       ##    ##  ##    ##
#      #######   ######  ######## ##     ##  ######



    def usersPage(self):
        self.data['users'] = model.getUsers()
        return render_template('acp/users/list.html', **self.data)

    def userAddPage(self):
        self.data['groups'] = config.USERS_GROUPS
        return render_template('acp/users/add.html', **self.data)

    def userEditPage(self, user_id):
        if not validation.userID(user_id): return abort(404)
        user = model.getUser(user_id)
        if not user: return abort(404)
        self.data['user'] = user
        self.data['groups'] = config.USERS_GROUPS
        return render_template('acp/users/edit.html', **self.data)

    def user_add_phone_numberPage(self, user_id):
        if not validation.userID(user_id): return False
        self.data['user_id'] = user_id
        return render_template('acp/users/add_phone_number.html', **self.data)

    def user_add_emailPage(self, user_id):
        if not validation.userID(user_id): return False
        self.data['user_id'] = user_id
        return render_template('acp/users/add_email.html', **self.data)

    def addUser(self, form):
        data = helper.prepareUserFormData(form)
        if helper.validAddUserData(data):
            data = helper.prepareAddUserData(data)
            model.addUser(data)

    def editUser(self, form):
        data = helper.prepareUserFormData(form)
        if helper.validEditUserData(data):
            data = helper.prepareEditUserData(data)
            model.editUser(data)

    def deleteUser(self, user_id):
        if validation.userID(user_id): return model.deleteUser(user_id)
        return False

    def addUserPhoneNumber(self, form):
        data = helper.prepareUserFormData(form)
        if validation.addUserPhoneNumberData(data):
            data = helper.prepareAddUserPhoneNumberData(data)
            model.addUserPhoneNumber(data)

    def addUserEmail(self, form):
        data = helper.prepareUserFormData(form)
        if validation.addUserEmailData(data):
            data = helper.prepareAddUserEmailData(data)
            model.addUserEmail(data)



#     ##     ## ######## ##    ## ##     ##  ######
#     ###   ### ##       ###   ## ##     ## ##    ##
#     #### #### ##       ####  ## ##     ## ##
#     ## ### ## ######   ## ## ## ##     ##  ######
#     ##     ## ##       ##  #### ##     ##       ##
#     ##     ## ##       ##   ### ##     ## ##    ##
#     ##     ## ######## ##    ##  #######   ######



    def menusPage(self):
        menus, menus_order = model.getMenus(self.current_language, order_by='id', order_type='asc')
        self.data['menus'] = menus
        self.data['menus_order'] = menus_order
        self.data['menu_item_names'] = model.getMenuItemNames(self.current_language)
        return render_template('acp/menus/list.html', **self.data)

    def menusAddPage(self):
        menus, menus_order = model.getMenus(self.current_language, order_by='id', order_type='asc')
        self.data['menus'] = menus
        self.data['menus_order'] = menus_order
        self.data['languages'] = config.LANGUAGES
        return render_template('acp/menus/add.html', **self.data)

    def addMenuItem(self, form):
        data = helper.prepareMenuItemFormData(form)
        if helper.validAddMenuItemData(data):
            data = helper.prepareAddMenuItemData(data)
            model.addMenuItem(data)

    def menusEditPage(self, item_id):
        if not validation.menuItemID(item_id): return abort(404)
        current_item = model.getMenuItem(item_id)
        if not current_item: return abort(404)
        self.data['current_item'] = current_item
        menus, menus_order = model.getMenus(self.current_language, order_by='id', order_type='asc')
        self.data['menus'] = menus
        self.data['menus_order'] = menus_order
        self.data['languages'] = config.LANGUAGES
        return render_template('acp/menus/edit.html', **self.data)

    def editMenuItem(self, form):
        data = helper.prepareMenuItemFormData(form)
        if helper.validEditMenuItemData(data):
            data = helper.prepareEditMenuItemData(data)
            model.editMenuItem(data)

    def deleteMenuItem(self, item_id):
        if validation.menuItemID(item_id): return model.deleteMenuItem(item_id)
        return False



#      ######  ##     ## ########  ########  ######## ##    ##  ######  #### ########  ######
#     ##    ## ##     ## ##     ## ##     ## ##       ###   ## ##    ##  ##  ##       ##    ##
#     ##       ##     ## ##     ## ##     ## ##       ####  ## ##        ##  ##       ##
#     ##       ##     ## ########  ########  ######   ## ## ## ##        ##  ######    ######
#     ##       ##     ## ##   ##   ##   ##   ##       ##  #### ##        ##  ##             ##
#     ##    ## ##     ## ##    ##  ##    ##  ##       ##   ### ##    ##  ##  ##       ##    ##
#      ######   #######  ##     ## ##     ## ######## ##    ##  ######  #### ########  ######



    def currenciesPage(self):
        self.data['currencies'] = model.getCurrencies(order_by='order', order_type='desc')
        return render_template('acp/currencies/list.html', **self.data)

    def currenciesAddPage(self):
        return render_template('acp/currencies/add.html', **self.data)

    def addCurrency(self, form):
        data = helper.prepareCurrencyFormData(form)
        if helper.validAddCurrencyData(data):
            data = helper.prepareAddCurrencyData(data)
            model.addCurrency(data)

    def currenciesEditPage(self, code):
        if not validation.currencyCode(code): return abort(404)
        self.data['currency'] = model.getCurrency(code.upper())
        if not self.data['currency']: return abort(404)
        return render_template('acp/currencies/edit.html', **self.data)

    def editCurrency(self, form):
        data = helper.prepareCurrencyFormData(form)
        if helper.validEditCurrencyData(data):
            data = helper.prepareEditCurrencyData(data)
            model.editCurrency(data)

    def deleteCurrency(self, code):
        if validation.currencyCode(code): return model.deleteCurrency(code)
        return False



#     ##          ###    ##    ##  ######   ##     ##    ###     ######   ########  ######
#     ##         ## ##   ###   ## ##    ##  ##     ##   ## ##   ##    ##  ##       ##    ##
#     ##        ##   ##  ####  ## ##        ##     ##  ##   ##  ##        ##       ##
#     ##       ##     ## ## ## ## ##   #### ##     ## ##     ## ##   #### ######    ######
#     ##       ######### ##  #### ##    ##  ##     ## ######### ##    ##  ##             ##
#     ##       ##     ## ##   ### ##    ##  ##     ## ##     ## ##    ##  ##       ##    ##
#     ######## ##     ## ##    ##  ######    #######  ##     ##  ######   ########  ######



    def languagesPage(self):
        self.data['languages'] = model.getLanguages(order_by='order', order_type='desc')
        return render_template('acp/languages/list.html', **self.data)

    def languagesAddPage(self):
        return render_template('acp/languages/add.html', **self.data)

    def addLanguage(self, form):
        data = helper.prepareLanguageFormData(form)
        if helper.validAddLanguageData(data):
            data = helper.prepareAddLanguageData(data)
            model.addLanguage(data)

    def languagesEditPage(self, code):
        if not validation.currencyCode(code): return abort(404)
        self.data['language'] = model.getLanguage(code.upper())
        if not self.data['language']: return abort(404)
        return render_template('acp/languages/edit.html', **self.data)

    def editLanguage(self, form):
        data = helper.prepareLanguageFormData(form)
        if helper.validEditLanguageData(data):
            data = helper.prepareEditLanguageData(data)
            model.editLanguage(data)

    def deleteLanguage(self, code):
        if validation.currencyCode(code): return model.deleteLanguage(code)
        return False
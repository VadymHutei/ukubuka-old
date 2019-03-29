from flask import render_template, abort
import config
import modules.acp.model as model
import modules.acp.helper as helper
import modules.validation as validation

class Acp():

    def __init__(self, lang=config.DEFAULT_LANGUAGE):
        self.current_language = lang if lang in config.LANGUAGES else config.DEFAULT_LANGUAGE
        self.data = {
            'menus': model.getMenus(self.current_language),
            'site_name': config.SITE_NAME
        }



#        ###    ##     ## ######## ##     ## ######## ##    ## ######## ####  ######     ###    ######## ####  #######  ##    ##
#       ## ##   ##     ##    ##    ##     ## ##       ###   ##    ##     ##  ##    ##   ## ##      ##     ##  ##     ## ###   ##
#      ##   ##  ##     ##    ##    ##     ## ##       ####  ##    ##     ##  ##        ##   ##     ##     ##  ##     ## ####  ##
#     ##     ## ##     ##    ##    ######### ######   ## ## ##    ##     ##  ##       ##     ##    ##     ##  ##     ## ## ## ##
#     ######### ##     ##    ##    ##     ## ##       ##  ####    ##     ##  ##       #########    ##     ##  ##     ## ##  ####
#     ##     ## ##     ##    ##    ##     ## ##       ##   ###    ##     ##  ##    ## ##     ##    ##     ##  ##     ## ##   ###
#     ##     ##  #######     ##    ##     ## ######## ##    ##    ##    ####  ######  ##     ##    ##    ####  #######  ##    ##



    def authentication_page(self):
        return render_template('acp/authentication.html', **self.data)



#     ########     ###     ######  ##     ## ########   #######     ###    ########  ########
#     ##     ##   ## ##   ##    ## ##     ## ##     ## ##     ##   ## ##   ##     ## ##     ##
#     ##     ##  ##   ##  ##       ##     ## ##     ## ##     ##  ##   ##  ##     ## ##     ##
#     ##     ## ##     ##  ######  ######### ########  ##     ## ##     ## ########  ##     ##
#     ##     ## #########       ## ##     ## ##     ## ##     ## ######### ##   ##   ##     ##
#     ##     ## ##     ## ##    ## ##     ## ##     ## ##     ## ##     ## ##    ##  ##     ##
#     ########  ##     ##  ######  ##     ## ########   #######  ##     ## ##     ## ########



    def dashboard_page(self):
        return render_template('acp/dashboard.html', **self.data)



#      ######     ###    ######## ########  ######    #######  ########  #### ########  ######
#     ##    ##   ## ##      ##    ##       ##    ##  ##     ## ##     ##  ##  ##       ##    ##
#     ##        ##   ##     ##    ##       ##        ##     ## ##     ##  ##  ##       ##
#     ##       ##     ##    ##    ######   ##   #### ##     ## ########   ##  ######    ######
#     ##       #########    ##    ##       ##    ##  ##     ## ##   ##    ##  ##             ##
#     ##    ## ##     ##    ##    ##       ##    ##  ##     ## ##    ##   ##  ##       ##    ##
#      ######  ##     ##    ##    ########  ######    #######  ##     ## #### ########  ######



    def categoriesPage(self, parent=None):
        if parent is None or not validation.categoryID(parent):
            categories = model.getCategories(self.current_language)
        else:
            categories = model.getCategories(self.current_language, parent)
            parent = model.getCategory(parent)
        self.data['categories'] = categories
        self.data['parent'] = parent
        self.data['category_names'] = model.getCategoryNames(self.current_language)
        return render_template('acp/categories/categories.html', **self.data)

    def addCategoryPage(self):
        self.data['categories'] = model.getCategories(self.current_language)
        self.data['languages'] = config.LANGUAGES
        return render_template('acp/categories/add.html', **self.data)

    def editCategoryPage(self, category_id):
        if not validation.categoryID(category_id): return abort(404)
        category = model.getCategory(category_id)
        if not category: return abort(404)
        self.data['categories'] = model.getCategories(self.current_language)
        self.data['category'] = category
        self.data['languages'] = config.LANGUAGES
        return render_template('acp/categories/edit.html', **self.data)

    def addCategory(self, form):
        data = helper.prepareCategoryFormData(form)
        if helper.validAddCategoryData(data):
            data = helper.prepareAddCategoryData(data)
            model.addCategory(data)

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
        return render_template('acp/products/products.html', **self.data)

    def addProductPage(self):
        self.data['categories'] = model.getCategories(self.current_language)
        self.data['languages'] = config.LANGUAGES
        return render_template('acp/products/add.html', **self.data)



#     ##     ##  ######  ######## ########   ######
#     ##     ## ##    ## ##       ##     ## ##    ##
#     ##     ## ##       ##       ##     ## ##
#     ##     ##  ######  ######   ########   ######
#     ##     ##       ## ##       ##   ##         ##
#     ##     ## ##    ## ##       ##    ##  ##    ##
#      #######   ######  ######## ##     ##  ######



    def users_page(self):
        self.data['users'] = model.getUsers()
        return render_template('acp/users/users.html', **self.data)

    def user_add_page(self):
        self.data['groups'] = config.USERS_GROUPS
        return render_template('acp/users/add.html', **self.data)

    def user_edit_page(self, user_id):
        if not validation.userID(user_id): return abort(404)
        user = model.getUser(user_id)
        if not user: return abort(404)
        self.data['user'] = user
        self.data['groups'] = config.USERS_GROUPS
        return render_template('acp/users/edit.html', **self.data)

    def user_add_phone_number_page(self, user_id):
        if not validation.userID(user_id): return False
        self.data['user_id'] = user_id
        return render_template('acp/users/add_phone_number.html', **self.data)

    def user_add_email_page(self, user_id):
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



    def menus_page(self):
        self.data['menu_item_names'] = model.getMenuItemNames(self.current_language)
        return render_template('acp/menus/menus.html', **self.data)

    def menus_add_page(self):
        self.data['languages'] = config.LANGUAGES
        return render_template('acp/menus/add.html', **self.data)

    def menus_edit_page(self, item_id):
        if not validation.menuItemID(item_id): return abort(404)
        self.data['current_item'] = model.getMenuItem(item_id)
        self.data['languages'] = config.LANGUAGES
        return render_template('acp/menus/edit.html', **self.data)

    def addMenuItem(self, form):
        data = helper.prepareMenuItemFormData(form)
        if helper.validAddMenuItemData(data):
            data = helper.prepareAddMenuItemData(data)
            model.addMenuItem(data)

    def editMenuItem(self, form):
        data = helper.prepareMenuItemFormData(form)
        if helper.validEditMenuItemData(data):
            data = helper.prepareEditMenuItemData(data)
            model.editMenuItem(data)

    def deleteMenuItem(self, item_id):
        if validation.menuItemID(item_id): return model.deleteMenuItem(item_id)
        return False
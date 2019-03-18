from flask import render_template, abort
import config
import modules.acp.model as model
import modules.acp.helper as helper
import modules.validation as validation

class Acp():

    def __init__(self, lang=config.DEFAULT_LANGUAGE):
        self.lang = lang if config.LANGUAGES else config.DEFAULT_LANGUAGE
        self.data = {
            'menus': model.getMenus(self.lang),
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
            categories = model.getCategories(self.lang)
        else:
            categories = model.getCategories(self.lang, parent)
            parent = model.getCategory(parent)
        self.data['categories'] = categories
        self.data['parent'] = parent
        return render_template('acp/categories/categories.html', **self.data)

    def addCategoryPage(self):
        self.data['categories'] = model.getCategories(self.lang)
        return render_template('acp/categories/add.html', **self.data)

    def editCategoryPage(self, category_id):
        if not validation.categoryID(category_id): return abort(404)
        category = model.getCategory(category_id)
        if not category: return abort(404)
        self.data['categories'] = model.getCategories(self.lang)
        self.data['category'] = category
        return render_template('acp/categories/edit.html', **self.data)

    def addCategory(self, form):
        data = helper.prepareCategoryFormData(form)
        if helper.validAddCategoryData(data):
            data = helper.prepareAddCategoryData(data)
            model.addCategory(data)

    def editCategory(self, form):
        data = helper.prepareCategoryFormData(form)
        print(data)
        if helper.validEditCategoryData(data):
            data = helper.prepareEditCategoryData(data)
            print(data)
            model.editCategory(data)

    def deleteCategory(self, category_id):
        if validation.categoryID(category_id): return model.deleteCategory(category_id)
        return False


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
        return render_template('acp/menus/menus.html', **self.data)

    def menus_add_page(self):
        return render_template('acp/menus/add.html', **self.data)

    def menus_edit_page(self, item_id):
        if not validation.menuItemID(item_id): return 'invalid ID'
        menu_item_data = model.getMenuItem(item_id)
        self.data['item'] = menu_item_data
        return render_template('acp/menus/edit.html', **self.data)

    def addMenuItem(self, form):
        data = helper.prepareMenuItemFormData(form)
        if validation.addMenuItemData(data):
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



#      ######  ######## ######## ######## #### ##    ##  ######    ######
#     ##    ## ##          ##       ##     ##  ###   ## ##    ##  ##    ##
#     ##       ##          ##       ##     ##  ####  ## ##        ##
#      ######  ######      ##       ##     ##  ## ## ## ##   ####  ######
#           ## ##          ##       ##     ##  ##  #### ##    ##        ##
#     ##    ## ##          ##       ##     ##  ##   ### ##    ##  ##    ##
#      ######  ########    ##       ##    #### ##    ##  ######    ######



    def settings_page(self):
        settings = model.getSettings()
        self.data['settings'] = settings
        return render_template('acp/settings/settings.html', **self.data)

    def saveSettings(self, form):
        data = form.to_dict()
        if validation.saveSettingsData(data):
            settings = model.getSettings()
            data = helper.prepareSaveSettingsData(settings, data)
            if data:
                model.saveSettings(data)
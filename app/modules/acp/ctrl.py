from flask import render_template
import config
import modules.acp.model as model
import modules.acp.helper as helper

class Acp():

    def __init__(self, lang=config.default_language):
        self.lang = lang if config.languages else config.default_language
        self.data = {
            'menus': model.getMenus(self.lang),
            'site_name': config.site_name
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



#     ##     ##  ######  ######## ########   ######
#     ##     ## ##    ## ##       ##     ## ##    ##
#     ##     ## ##       ##       ##     ## ##
#     ##     ##  ######  ######   ########   ######
#     ##     ##       ## ##       ##   ##         ##
#     ##     ## ##    ## ##       ##    ##  ##    ##
#      #######   ######  ######## ##     ##  ######



    def users_page(self):
        users = model.getUsers()
        self.data['users'] = users
        return render_template('acp/users/users.html', **self.data)

    def user_add_page(self):
        groups = model.getUsersGroups()
        self.data['groups'] = groups
        return render_template('acp/users/add.html', **self.data)

    def user_edit_page(self, user_id):
        if not helper.validUserID(user_id): return False
        user = model.getUser(user_id)
        groups = model.getUsersGroups()
        self.data['user'] = user
        self.data['groups'] = groups
        return render_template('acp/users/edit.html', **self.data)

    def user_add_phone_number_page(self, user_id):
        if not helper.validUserID(user_id): return False
        self.data['user_id'] = user_id
        return render_template('acp/users/add_phone_number.html', **self.data)

    def user_add_email_page(self, user_id):
        if not helper.validUserID(user_id): return False
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
        if helper.validUserID(user_id): return model.deleteUser(user_id)
        return False

    def addUserPhoneNumber(self, form):
        data = helper.prepareUserFormData(form)
        if helper.validAddUserPhoneNumberData(data):
            data = helper.prepareAddUserPhoneNumberData(data)
            model.addUserPhoneNumber(data)

    def addUserEmail(self, form):
        data = helper.prepareUserFormData(form)
        if helper.validAddUserEmailData(data):
            data = helper.prepareAddUserEmailData(data)
            model.addUserEmail(data)



#     ##     ##  ######  ######## ########   ######      ######   ########   #######  ##     ## ########   ######
#     ##     ## ##    ## ##       ##     ## ##    ##    ##    ##  ##     ## ##     ## ##     ## ##     ## ##    ##
#     ##     ## ##       ##       ##     ## ##          ##        ##     ## ##     ## ##     ## ##     ## ##
#     ##     ##  ######  ######   ########   ######     ##   #### ########  ##     ## ##     ## ########   ######
#     ##     ##       ## ##       ##   ##         ##    ##    ##  ##   ##   ##     ## ##     ## ##              ##
#     ##     ## ##    ## ##       ##    ##  ##    ##    ##    ##  ##    ##  ##     ## ##     ## ##        ##    ##
#      #######   ######  ######## ##     ##  ######      ######   ##     ##  #######   #######  ##         ######



    def users_groups_page(self):
        groups = model.getUsersGroups()
        self.data['users_groups'] = groups
        return render_template('acp/users/groups/groups.html', **self.data)

    def users_groups_add_page(self):
        return render_template('acp/users/groups/add.html', **self.data)

    def users_groups_edit_page(self, group_id):
        if not helper.validUsersGroupID(group_id): return 'invalid ID'
        group = model.getUsersGroup(group_id)
        self.data['group'] = group
        return render_template('acp/users/groups/edit.html', **self.data)

    def addUsersGroup(self, form):
        data = helper.prepareUsersGroupFormData(form)
        if helper.validAddUsersGroupData(data):
            data = helper.prepareAddUsersGroupData(data)
            model.addUsersGroup(data)

    def editUsersGroup(self, form):
        data = helper.prepareUsersGroupFormData(form)
        if helper.validEditUsersGroupData(data):
            data = helper.prepareEditUsersGroupData(data)
            model.editUsersGroup(data)

    def deleteUsersGroup(self, users_group_id):
        if helper.validUsersGroupID(users_group_id): return model.deleteUsersGroup(users_group_id)
        return False



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
        if not helper.validMenuItemID(item_id): return 'invalid ID'
        menu_item_data = model.getMenuItem(item_id)
        self.data['item'] = menu_item_data
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
        if helper.validMenuItemID(item_id): return model.deleteMenuItem(item_id)
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
        if helper.validSaveSettingsData(data):
            settings = model.getSettings()
            data = helper.prepareSaveSettingsData(settings, data)
            if data:
                model.saveSettings(data)
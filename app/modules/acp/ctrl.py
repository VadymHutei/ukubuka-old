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

    def users(self):
        return render_template('acp/users/users.html', **self.data)

    def users_add(self):
        return render_template('acp/users/add.html', **self.data)

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
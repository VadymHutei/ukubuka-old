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
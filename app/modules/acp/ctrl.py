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

    def dashboard(self):
        return render_template('acp/dashboard.html', **self.data)

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
        self.data['item'] = model.getMenuItem(item_id)
        return render_template('acp/menus/edit.html', **self.data)

    def addMenuItem(self, form):
        data = helper.prepareMenuItemData(form)
        if data: return model.addMenuItem(**data)
        return False

    def editMenuItem(self, form):
        data = helper.prepareMenuItemData(form)
        if data: return model.editMenuItem(**data)
        return False
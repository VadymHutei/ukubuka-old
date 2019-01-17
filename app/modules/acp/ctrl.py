from flask import render_template
import config
import modules.acp.model as model
import modules.acp.helper as helper

class Acp():

    def __init__(self, lang=config.default_language):
        self.lang = lang if config.languages else config.default_language
        self.data = {
            'menu': [],
            'site_name': config.site_name
        }

    def dashboard(self):
        return render_template('acp/dashboard.html', **self.data)

    def users(self):
        return render_template('acp/users/users.html', **self.data)

    def users_add(self):
        return render_template('acp/users/add.html', **self.data)

    def menus_add(self):
        self.data['menus'] = model.getMenus(self.lang)
        return render_template('acp/menus/add.html', **self.data)

    def addMenuItem(self, form_data):
        data = {}
        menu = form_data.get('menu', '')
        if not helper.validMenuName(menu): return False, 'invalid menu'
        data['menu'] = menu
        parent = form_data.get('parent', '')
        if parent:
            if not helper.validMenuParent(parent): return False, 'invalid parent'
            data['parent'] = int(parent)
        name_ukr = form_data.get('name_ukr', '')
        if not helper.validMenuItemName(name_ukr): return False, 'invalid ukrainian name'
        data['name_ukr'] = name_ukr
        name_eng = form_data.get('name_eng', '')
        if not helper.validMenuItemName(name_eng): return False, 'invalid english name'
        data['name_eng'] = name_eng
        link = form_data.get('link')
        if link:
            if not helper.validMenuItemLink(link): return False, 'invalid link'
            data['link'] = '/' + link.lstrip('/')
        is_active = 'Y' if form_data.get('is_active', 'off') == 'on' else 'N'
        data['is_active'] = is_active
        model.addMenuItem(**data)
        return True, 'success'
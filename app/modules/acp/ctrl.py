from flask import render_template
import config
from modules.acp.model import *

class Acp():

    def __init__(self, lang='ukr'):
        self.lang = lang if lang in ('ukr', 'eng') else 'ukr'
        self.data = {
            'menu': getMenu(self.lang),
            'site_name': config.site_name
        }

    def dashboard(self):
        return render_template('acp/dashboard.html', **self.data)

    def users(self):
        return render_template('acp/users/users.html', **self.data)

    def users_add(self):
        return render_template('acp/users/add.html', **self.data)

    def menus_add(self):
        menus = getMenusList()
        self.data['menus_list'] = menus
        return render_template('acp/menus/add.html', **self.data)
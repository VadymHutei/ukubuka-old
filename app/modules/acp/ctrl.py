from flask import render_template
import config

class Acp():

    def __init__(self):
        pass

    def dashboard(self):
        return render_template('acp/dashboard.html', site_name=config.site_name)
from flask import render_template
import config
import modules.main.model as model
import modules.main.helper as helper

class Main():

    def __init__(self):
        self.data = {}

    def main_page(self):
        return render_template('site/main/main.html', **self.data)
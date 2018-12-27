from flask import Flask, request, redirect, url_for, abort, render_template
import config
from modules.main.ctrl import Main

app = Flask(__name__)

@app.route('/')
def main():
    main = Main()
    if main.view:
        return main.view
    else:
        return 'error'

@app.route('/test')
def test_wol():
    return redirect(url_for('test', lang='uk'))

@app.route('/<lang>/test')
def test(lang):
    if len(lang) != 2:
        abort(400)
    if lang not in config.languages:
        return redirect(url_for('test', lang='uk'))
    return lang

@app.errorhandler(400)
def page_not_found(error):
    return render_template('errors/bad_request.html'), 400

if __name__ == "__main__":
    app.run(**config.app_config)
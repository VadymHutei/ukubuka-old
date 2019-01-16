from flask import Flask, request, redirect, url_for, abort, render_template
import config
from modules.main.ctrl import Main
from modules.acp.ctrl import Acp

app = Flask(__name__)

#
#
#     ___       ___   ____    ________   ____     _______     __________   ____
#     `MMb     dMM'  6MMMMb   `MMMMMMMb. `MM'     `M'`MM'     `MMMMMMMMM  6MMMMb\
#      MMM.   ,PMM  8P    Y8   MM    `Mb  MM       M  MM       MM      \ 6M'    `
#      M`Mb   d'MM 6M      Mb  MM     MM  MM       M  MM       MM        MM
#      M YM. ,P MM MM      MM  MM     MM  MM       M  MM       MM    ,   YM.
#      M `Mb d' MM MM      MM  MM     MM  MM       M  MM       MMMMMMM    YMMMMb
#      M  YM.P  MM MM      MM  MM     MM  MM       M  MM       MM    `        `Mb
#      M  `Mb'  MM MM      MM  MM     MM  MM       M  MM       MM              MM
#      M   YP   MM YM      M9  MM     MM  YM       M  MM       MM              MM
#      M   `'   MM  8b    d8   MM    .M9   8b     d8  MM    /  MM      / L    ,M9
#     _M_      _MM_  YMMMM9   _MMMMMMM9'    YMMMMM9  _MMMMMMM _MMMMMMMMM MYMMMM9
#
#
#

#     ##     ##    ###    #### ##    ##
#     ###   ###   ## ##    ##  ###   ##
#     #### ####  ##   ##   ##  ####  ##
#     ## ### ## ##     ##  ##  ## ## ##
#     ##     ## #########  ##  ##  ####
#     ##     ## ##     ##  ##  ##   ###
#     ##     ## ##     ## #### ##    ##

@app.route('/')
def main():
    main = Main()
    return main.view

#     ######## ########  ######  ########
#        ##    ##       ##    ##    ##
#        ##    ##       ##          ##
#        ##    ######    ######     ##
#        ##    ##             ##    ##
#        ##    ##       ##    ##    ##
#        ##    ########  ######     ##

@app.route('/test')
def test():
    return 'test'

#        ###     ######  ########
#       ## ##   ##    ## ##     ##
#      ##   ##  ##       ##     ##
#     ##     ## ##       ########
#     ######### ##       ##
#     ##     ## ##    ## ##
#     ##     ##  ######  ##

@app.route('/acp', methods=['GET'])
def acp():
    acp = Acp()
    return acp.dashboard()

#
#
#     __________ ________    ________       ____    ________      ____
#     `MMMMMMMMM `MMMMMMMb.  `MMMMMMMb.    6MMMMb   `MMMMMMMb.   6MMMMb\
#      MM      \  MM    `Mb   MM    `Mb   8P    Y8   MM    `Mb  6M'    `
#      MM         MM     MM   MM     MM  6M      Mb  MM     MM  MM
#      MM    ,    MM     MM   MM     MM  MM      MM  MM     MM  YM.
#      MMMMMMM    MM    .M9   MM    .M9  MM      MM  MM    .M9   YMMMMb
#      MM    `    MMMMMMM9'   MMMMMMM9'  MM      MM  MMMMMMM9'       `Mb
#      MM         MM  \M\     MM  \M\    MM      MM  MM  \M\          MM
#      MM         MM   \M\    MM   \M\   YM      M9  MM   \M\         MM
#      MM      /  MM    \M\   MM    \M\   8b    d8   MM    \M\  L    ,M9
#     _MMMMMMMMM _MM_    \M\__MM_    \M\_  YMMMM9   _MM_    \M\_MYMMMM9
#
#
#
@app.errorhandler(400)
def page_not_found(error):
    return render_template('errors/bad_request.html'), 400

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/not_found.html'), 404

if __name__ == "__main__":
    app.run(**config.app_config)
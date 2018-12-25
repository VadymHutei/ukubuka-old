from flask import Flask, request
import config
from services import *

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World from Flask"

@app.route("/test")
def test():
    shop = Shop()
    return 'Hello test'

if __name__ == "__main__":
    app.run(**config.app_config)
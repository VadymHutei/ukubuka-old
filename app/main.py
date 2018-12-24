from flask import Flask
import config

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World from Flask"

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(**config.app_config)
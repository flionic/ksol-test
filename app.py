# app.py
from flask import Flask
app = Flask(__name__)


# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>First init</h1>"


if __name__ == '__main__':
    app.run(threaded=True, port=5000)

# app.py
from flask import Flask, render_template

app = Flask(__name__)


# A welcome message to test our server
@app.route('/')
def index():
    return render_template("layout/main.html")


if __name__ == '__main__':
    app.run(threaded=True, port=5000)

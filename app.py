# app.py
import hashlib

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


# A welcome message to test our server
@app.route('/')
def index():
    return render_template("payment.html")


def pay_sign(pay_request):
    secret = 'SecretKey01'
    keys_required = ["shop_id", "payway", "amount", "currency", "shop_order_id"]

    sign = hashlib.sha256()
    keys_required.sort()
    sign_values = [str(pay_request[i]) for i in keys_required]
    sign.update(':'.join(sign_values).encode())
    sign.update(secret.encode())

    return sign.hexdigest()


if __name__ == '__main__':
    app.run(threaded=True, port=5000)

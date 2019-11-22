# app.py
import hashlib

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


# A welcome message to test our server
@app.route('/')
def index():
    return render_template("payment.html")


@app.route('/action/payment', methods=['POST'])
def act_payment():
    # pm = payment
    pm_request = request.form.to_dict(flat=True)
    pm_request['shop_id'] = 5
    pm_request['shop_order_id'] = 101

    print(request.form)
    print(request.form.to_dict(flat=True))

    if request.form.get('currency') is None:
        return 404
    elif request.form.get('currency') == 'EUR':
        pm_request['currency'] = 978
        return piastix_form(pm_request)
    elif request.form.get('currency') == 'USD':
        pm_request['currency'] = 840
        return piastix_api_bill(pm_request)
    elif request.form.get('currency') == 'RUB':
        pm_request['currency'] = 643
        return piastix_api_invoice(pm_request)
    else:
        return jsonify({"response": 0})


def pm_sign(pay_request, keys_required):
    secret = 'SecretKey01'

    sign = hashlib.sha256()
    keys_required.sort()
    sign_values = [str(pay_request[i]) for i in keys_required]
    sign.update(':'.join(sign_values).encode())
    sign.update(secret.encode())

    return sign.hexdigest()


def piastix_form(payment):
    keys_required = ["amount", "currency", "shop_id", "shop_order_id"]
    payment['sign'] = pm_sign(payment, keys_required)

    return jsonify({'type': 'html', 'data': render_template('ajax/payform.html', payment=payment)})


def piastix_api_bill(payment):
    keys_required = ["amount", "currency", "shop_id", "shop_order_id"]

    return jsonify({"response": "piastix_api_bill"})


def piastix_api_invoice(payment):
    keys_required = ["shop_amount", "shop_currency", "shop_id", "shop_order_id", "payer_currency"]

    return jsonify({"response": "piastix_api_invoice"})


if __name__ == '__main__':
    app.run(threaded=True, port=5000)

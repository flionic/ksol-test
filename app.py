# app.py
import hashlib

import requests
from flask import Flask, render_template, jsonify, request, redirect

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


# TODO проверка по ключам
# TODO piastix Class + checker curr
# TODO flask redirects and more

def piastix_form(pm_request):
    keys_required = ["amount", "currency", "shop_id", "shop_order_id"]
    pm_request['sign'] = pm_sign(pm_request, keys_required)

    return jsonify({'response': 'piastix_api_bill', 'type': 'html', 'data': render_template('ajax/payform.html', payment=pm_request)})


def piastix_api_bill(pm_request):
    url = 'https://core.piastrix.com/bill/create'
    keys_required = ["shop_amount", "shop_currency", "shop_id", "shop_order_id", "payer_currency"]

    pm_request['shop_amount'] = pm_request.pop('amount')
    pm_request['payer_currency'] = pm_request.pop('currency')
    pm_request['shop_currency'] = pm_request['payer_currency']
    pm_request['sign'] = pm_sign(pm_request, keys_required)

    piastix_response = requests.post(url, json=pm_request)

    # TODO: редирект на url из ответа

    return jsonify({"response": "piastix_api_bill", "piastix_response": piastix_response.json(), "type": "url", "data": piastix_response.json()['data']['url']})


def piastix_api_invoice(pm_request):
    url = 'https://core.piastrix.com/invoice/create'
    keys_required = ["amount", "currency", "payway", "shop_id", "shop_order_id"]

    pm_request['payway'] = 'payeer_rub'
    pm_request['sign'] = pm_sign(pm_request, keys_required)

    piastix_response = requests.post(url, json=pm_request)

    # TODO: редирект на страницу оплаты платёжной

    return jsonify({"response": "piastix_api_invoice", "piastix_response": piastix_response.json(), "type": "url", "data": piastix_response.json()['data']['data']['referer']})


if __name__ == '__main__':
    app.run(threaded=True, port=5000)

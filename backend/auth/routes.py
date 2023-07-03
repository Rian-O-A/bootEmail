from flask import Blueprint, jsonify, request, render_template
from backend.Payment.obterPagamen import pesquisar_pagamento
from backend.Payment.processPayment import process_payment 
from backend.Payment.controlerPeding import statusPayment
from backend.credentials import public_key
import json


auth_route = Blueprint('auth', __name__)


@auth_route.route('/')
def home():
   return render_template('index.html', public_key=public_key)

@auth_route.route('/product', methods=['POST'])
def sendProduct():
    idPayment = request.json.get("idPayment")
    response = pesquisar_pagamento(idPayment)
    return jsonify({'Message': response[1]}), response[0]

@auth_route.route('/process_payment', methods=['POST'])
def add_income():
    request_values = request.get_json()
    # json.dump(request_values, open('forms.json', 'w', encoding="UTF-8"), indent=6, ensure_ascii=False)
    payment = process_payment(request_values)
    
    response = pesquisar_pagamento(payment["id"])
    return jsonify(payment), response[0]


@auth_route.route('/webhook', methods=['POST'])
def webhook():
    request_values = request.get_json()
    
    statusPayment(request_values["data"]["id"], request_values["action"])
    
    return jsonify({"Message":"ok"}), 200
# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: api.py
# Descripción: RESTful API de microservicio
# ============================================================
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, jsonify
import requests
from common.utils import get_host
from common.vars import GATEWAY_API_URL, USER_API_URL, PRODUCT_API_URL, PURCHASE_API_URL

app = Flask(__name__)

@app.route('/api/all')
def get_all():
    try:
        users_resp = requests.get(f"{USER_API_URL}/api/users")
        products_resp = requests.get(f"{PRODUCT_API_URL}/api/products")
        purchases_resp = requests.get(f"{PURCHASE_API_URL}/api/purchases")

        users = users_resp.json()
        products = products_resp.json()
        purchases = purchases_resp.json()

        return jsonify({
            "users": users,
            "products": products,
            "purchases": purchases
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Error comunicando con microservicios",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    app.run(port=get_host(GATEWAY_API_URL))
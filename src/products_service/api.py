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
from common.utils import load_item, get_host
from common.vars import PRODUCTS_FILE, PRODUCT_API_URL

app = Flask(__name__)

@app.route('/api/products', methods=['GET'])
def get_products():
    products = load_item(PRODUCTS_FILE)
    return jsonify(products)

if __name__ == '__main__':
    app.run(port=get_host(PRODUCT_API_URL))
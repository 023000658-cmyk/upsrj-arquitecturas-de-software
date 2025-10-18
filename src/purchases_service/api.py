# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: api.py
# Descripción: RESTful API del microservicio de compras
# ============================================================
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, jsonify, request
from common.utils import load_item, save_item, get_host
from common.vars import PURCHASES_FILE, PURCHASE_API_URL

app = Flask(__name__)

# Obtener todas las compras
@app.route('/api/purchases', methods=['GET'])
def get_purchases():
    purchases = load_item(PURCHASES_FILE)
    return jsonify(purchases)

# Crear una nueva compra vía API
@app.route('/api/purchases', methods=['POST'])
def create_purchase():
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if not product_id or not quantity:
        return jsonify({"error": "El ID del producto y la cantidad son requeridos"}), 400

    try:
        quantity = int(quantity)
    except ValueError:
        return jsonify({"error": "La cantidad debe ser un número entero"}), 400

    purchases = load_item(PURCHASES_FILE)
    purchase = {
        'id': len(purchases) + 1,
        'product_id': int(product_id),
        'quantity': quantity
    }
    purchases.append(purchase)
    save_item(PURCHASES_FILE, purchases)

    return jsonify(purchase), 201

if __name__ == '__main__':
    app.run(port=get_host(PURCHASE_API_URL))

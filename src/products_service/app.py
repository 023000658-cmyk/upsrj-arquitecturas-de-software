# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: app.py
# Descripción: Backend del microservicio
# ============================================================
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, render_template, redirect, url_for, jsonify
from common.utils import load_item, save_item, get_host
from common.vars import PRODUCTS_FILE, PRODUCT_SERVICE_URL

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
app = Flask(__name__, template_folder=template_dir)

@app.route('/products', methods=['GET'])
def get_products():
    products = load_item(PRODUCTS_FILE)
    return render_template("products.html", products=products)

@app.route('/products/create', methods=['GET'])
def create_product_form():
    return render_template("create_product.html")

@app.route('/products', methods=['POST'])
def create_product():
    name = request.form.get("name")
    if not name:
        return "El nombre del producto es requerido", 400

    products = load_item(PRODUCTS_FILE)
    product = {'id': len(products) + 1, 'name': name}
    products.append(product)
    save_item(PRODUCTS_FILE, products)

    return redirect(url_for('get_products'))

#------------------------------------------------------------------------------------
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    """Obtiene un producto por su ID"""
    products = load_item(PRODUCTS_FILE)
    product = next((p for p in products if p['id'] == product_id), None)
    
    if product is None:
        return jsonify({"error": "Producto no encontrado"}), 404

    return jsonify(product), 200
#------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(port=get_host(PRODUCT_SERVICE_URL))
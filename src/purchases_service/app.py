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
from flask import Flask, request, render_template, redirect, url_for
from common.utils import load_item, save_item, get_host
from common.vars import PURCHASES_FILE, PURCHASE_SERVICE_URL, USERS_FILE, PRODUCTS_FILE
from datetime import datetime

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
app = Flask(__name__, template_folder=template_dir)


# ============================================================
# RUTA: Mostrar todas las compras
# ============================================================
@app.route('/purchases', methods=['GET'])
def get_purchases():
    purchases = load_item(PURCHASES_FILE)
    return render_template("purchases.html", purchases=purchases)


# ============================================================
# RUTA: Formulario de creación
# ============================================================
@app.route('/purchases/create', methods=['GET'])
def create_purchase_form():
    return render_template("create_purchase.html")


# ============================================================
# RUTA: Crear una compra nueva
# ============================================================
@app.route('/purchases', methods=['POST'])
def create_purchase():
    users = load_item(USERS_FILE)
    products = load_item(PRODUCTS_FILE)

    user_id = request.form.get("user_id") or (request.json.get("user_id") if request.is_json else None)
    product_id = request.form.get("product_id") or (request.json.get("product_id") if request.is_json else None)

    if not user_id:
        return {"error": "user_id missing"}, 400
    if not product_id:
        return {"error": "product_id missing"}, 400

    if not any(u["id"] == int(user_id) for u in users):
        return {"error": "user not found"}, 404
    if not any(p["id"] == int(product_id) for p in products):
        return {"error": "product not found"}, 404

    purchases = load_item(PURCHASES_FILE)

    purchase = {
        "id": len(purchases) + 1,
        "user_id": int(user_id),
        "product_id": int(product_id),
        "timestamp": datetime.now().isoformat()
    }

    purchases.append(purchase)
    save_item(PURCHASES_FILE, purchases)

    user_index = int(user_id) - 1
    if "purchased_products" not in users[user_index]:
        users[user_index]["purchased_products"] = []
    users[user_index]["purchased_products"].append(int(product_id))
    save_item(USERS_FILE, users)

    # Siempre devolver 201, aunque sea HTML
    return render_template("purchases.html", purchases=purchases), 201



# ============================================================
# RUTA: Mostrar compras de un usuario
# ============================================================
@app.route('/purchases/<int:user_id>', methods=['GET'])
def get_purchases_by_user(user_id):
    purchases = load_item(PURCHASES_FILE)
    users = load_item(USERS_FILE)

    if not any(u["id"] == user_id for u in users):
        return {"error": "user not found"}, 404

    # Filtrar compras del usuario
    user_purchases = [p for p in purchases if p["user_id"] == user_id]

    # Renderizar la misma plantilla HTML que /purchases
    return render_template("purchases.html", purchases=user_purchases), 200

# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    app.run(port=get_host(PURCHASE_SERVICE_URL))

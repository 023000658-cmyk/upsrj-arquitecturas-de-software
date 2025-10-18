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
from flask import Flask, render_template
import requests
from common.utils import get_host
from common.vars import GATEWAY_SERVICE_URL, USER_API_URL, PRODUCT_API_URL, PURCHASE_API_URL

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/all')
def get_all():
    try:
        # Obtener usuarios, productos y compras desde sus APIs
        users_resp = requests.get(f"{USER_API_URL}/api/users")
        products_resp = requests.get(f"{PRODUCT_API_URL}/api/products")
        purchases_resp = requests.get(f"{PURCHASE_API_URL}/api/purchases")

        users = users_resp.json()
        products = products_resp.json()
        purchases = purchases_resp.json()


        return render_template("all.html", users=users, products=products)

    except requests.exceptions.RequestException as e:
        return render_template("error.html", error=str(e)), 500

if __name__ == '__main__':
    app.run(port=get_host(GATEWAY_SERVICE_URL))


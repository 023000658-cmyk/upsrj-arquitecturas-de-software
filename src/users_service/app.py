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
from common.vars import USERS_FILE, USER_SERVICE_URL

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
app = Flask(__name__, template_folder=template_dir)

@app.route('/users', methods=['GET'])
def get_users():
    users = load_item(USERS_FILE)
    return render_template("users.html", users=users)

@app.route('/users/create', methods=['GET'])
def create_user_form():
    return render_template("create_user.html")

@app.route('/users', methods=['POST'])
def create_user():
    name = request.form.get("name")
    if not name:
        return "El nombre del usuario es requerido", 400

    users = load_item(USERS_FILE)
    user = {'id': len(users) + 1, 'name': name}
    users.append(user)
    save_item(USERS_FILE, users)

    return redirect(url_for('get_users'))

if __name__ == '__main__':
    app.run(port=get_host(USER_SERVICE_URL))
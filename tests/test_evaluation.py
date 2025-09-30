# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: test_evaluation.py
# Descripción: Archivo de pruebas unitarias para validar el comportamiento de funciones del proyecto
# ============================================================
import sys, os, unittest, io
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import importlib.util

BASE_DIR =os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Colores ANSI
GREEN = "\033[92m"
RED = "\033[91m"
LIGHT_RED = "\033[31m"
BLUE = "\033[34m"
RESET = "\033[0m"
BOLD = "\033[1m"
SEPARATOR = f"{BOLD}{'='*50}{RESET}"

def load_flask_app(name, relative_path):
    full_path = os.path.join(BASE_DIR, relative_path)
    print(f"{BLUE}[DEBUG] Buscando: {full_path}{RESET}")
    if not os.path.exists(full_path):
        print(f"{RED}[ERROR] No se encontró: {full_path}{RESET}")
        return None

    try:
        service_dir = os.path.dirname(full_path)
        if service_dir not in sys.path:
            sys.path.insert(0, service_dir)

        spec = importlib.util.spec_from_file_location(name, full_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "app"):
                return module.app
            else:
                print(f"{RED}[ERROR] El módulo {name} no tiene atributo 'app'{RESET}")
    except Exception as e:
        print(f"{RED}[ERROR] Fallo al importar {name}: {e}{RESET}")

    return None

users_app = load_flask_app("users", "users_service/app.py")
products_app = load_flask_app("products", "products_service/app.py")
purchases_app = load_flask_app("purchases", "purchases_service/app.py")
gateway_app = load_flask_app("gateway", "gateway/app.py")

USERS_AVAILABLE = users_app is not None
PRODUCTS_AVAILABLE = products_app is not None
PURCHASES_AVAILABLE = purchases_app is not None
GATEWAY_AVAILABLE = gateway_app is not None

class CustomTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.successes = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.successes.append((test))

class CustomTestRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return CustomTestResult(self.stream, self.descriptions, self.verbosity)
    
class TestEvaluation(unittest.TestCase):
    
    def setUp(self):
        test_name = self._testMethodName

        if "user" in test_name:
            if not USERS_AVAILABLE:
                self.fail("El microservicio users_service no está disponible o mal estructurado.")
            self.app = users_app.test_client()

        elif "product" in test_name:
            if not PRODUCTS_AVAILABLE:
                self.fail("El microservicio products_service no está disponible o mal estructurado.")
            self.app = products_app.test_client()

        elif "purchase" in test_name:
            if not PURCHASES_AVAILABLE:
                self.fail("El microservicio purchases_service no está disponible o mal estructurado.")
            self.app = purchases_app.test_client()

        elif "gateway" in test_name:
            if not GATEWAY_AVAILABLE:
                self.fail("El microservicio gateway no está disponible o mal estructurado.")
            self.app = gateway_app.test_client()

        else:
            self.app = None

        if self.app:
            self.app.testing = True

    def test_get_users_route(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Usuarios', response.data)  # Ajusta según el contenido HTML

    def test_create_user_missing_name(self):
        response = self.app.post('/users', data={})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'requerido', response.data)

    def test_create_user_valid(self):
        response = self.app.post('/users', data={"name": "Carlos"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Carlos', response.data)

    def test_get_products_route(self):
        response = self.app.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Productos', response.data)

    def test_create_product_missing_fields(self):
        response = self.app.post('/products', data={})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'requerido', response.data)

    def test_create_product_valid(self):
        response = self.app.post('/products', data={"name": "Laptop", "price": "1200"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Laptop', response.data)

    def test_get_purchases_by_user(self):
        response = self.app.get('/purchases/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Compras', response.data)

    def test_create_purchase_missing_fields(self):
        response = self.app.post('/purchases', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'user_id', response.data)

    def test_create_purchase_invalid_user(self):
        response = self.app.post('/purchases', json={"user_id": 999, "product_id": 3})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"usuario", response.data.lower())

    def test_create_purchase_invalid_product(self):
        response = self.app.post('/purchases', json={"user_id": 1, "product_id": 999})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"producto", response.data.lower())

    def test_create_purchase_valid(self):
        response = self.app.post('/purchases', json={"user_id": 1, "product_id": 3})
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'"user_id": 1', response.data.decode())


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestEvaluation)
    silent_stream = io.StringIO()
    runner = CustomTestRunner(stream=silent_stream, verbosity=0)
    result = runner.run(suite)

    print(f"{BOLD}EVALUACION{RESET}")
    # Resultados individuales
    print(SEPARATOR)
    print(f"{BOLD}Resultados individuales:{RESET}")
    for test_case in result.successes:
        print(f"{test_case._testMethodName}: {GREEN}{BOLD}PASSED{RESET}")

    for test_case, traceback in result.failures + result.errors:
        print(f"{test_case._testMethodName}: {RED}{BOLD}FAILED{RESET}")
        # Extraer solo el mensaje de la última línea del traceback
        last_line = traceback.strip().split('\n')[-1]
        mensaje = last_line.split(':')[-1].strip()
        print(f"- detalles: {LIGHT_RED}{mensaje}{RESET}")

    # Resumen final
    print(SEPARATOR)
    print(f"{BOLD}Resumen final:{RESET}")
    if result.wasSuccessful():
        print(f"{GREEN}{BOLD}SUCCESS:{RESET} Todos los tests pasaron correctamente.")
    else:
        print(f"{RED}{BOLD}FAILED:{RESET} Uno o más tests fallaron.")
    print(SEPARATOR)

    sys.exit(not result.wasSuccessful())
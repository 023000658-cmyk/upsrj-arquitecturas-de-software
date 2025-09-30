import os

# REPOSITORY FILES
PRODUCTS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "products_service", "products.json")
USERS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "users_service", "users.json")

# SERVICE URL's
GATEWAY_SERVICE_URL = "http://localhost:5000"
USER_SERVICE_URL = "http://localhost:5002"
PRODUCT_SERVICE_URL = "http://localhost:5004"

# REST API URL's 
GATEWAY_API_URL = "http://localhost:5001"
USER_API_URL = "http://localhost:5003"
PRODUCT_API_URL = "http://localhost:5005"
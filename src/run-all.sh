#!/bin/bash

# ============================================================
# Politécnica de Santa Rosa
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: run_all.sh
# Descripción: Levanta todos los microservicios en terminales separadas
# ============================================================

# Ruta base del proyecto
BASE_DIR=$(pwd)

# Crear carpeta de logs si no existe
mkdir -p logs

# Microservicios
declare -A SERVICES=(
  ["Users Service"]="src/users_service/app.py"
  ["Users API"]="src/users_service/api.py" 
  ["Products Service"]="src/products_service/app.py"
  ["Products API"]="src/products_service/api.py"
  ["Purchases Service"]="src/purchases_service/app.py"
  ["Purchases API"]="src/purchases_service/api.py"
  ["Gateway Web"]="src/gateway/app.py"
  ["Gateway API"]="src/gateway/api.py"
)

echo "Iniciando microservicios..."

for NAME in "${!SERVICES[@]}"; do
  FILE="${SERVICES[$NAME]}"
  echo "Lanzando $NAME → $FILE"
  nohup python "$FILE" > "logs/${NAME}.log" 2>&1 &
  sleep 1
done

echo -e "\nTodos los servicios han sido lanzados en terminales independientes."
echo "Revisa los logs en la carpeta ./logs/"

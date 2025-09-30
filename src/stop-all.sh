#!/bin/bash

# ============================================================
# Politécnica de Santa Rosa
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: stop-all.sh
# Descripción: Detiene todos los microservicios ejecutados con run-all.sh
# ============================================================

echo "Deteniendo microservicios..."

# Lista de archivos principales de cada microservicio
FILES=(
  "users_service/api.py"
  "users_service/app.py"
  "products_service/api.py"
  "products_service/app.py"
  #"purchases_service/api.py"
  #"purchases_service/app.py"
  "gateway/api.py"
  "gateway/app.py"
)

for FILE in "${FILES[@]}"; do
  PID=$(ps aux | grep "$FILE" | grep -v grep | awk '{print $2}')
  if [ -n "$PID" ]; then
    echo "Matando proceso $FILE (PID: $PID)"
    kill "$PID"
  else
    echo "No se encontró proceso para $FILE"
  fi
done

echo "Todos los microservicios han sido detenidos."
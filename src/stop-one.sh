#!/bin/bash

# ============================================================
# Politécnica de Santa Rosa
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: stop-one.sh
# Descripción: Detiene un microservicio
# ============================================================

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --service) SERVICES="$2"; shift ;;
        *) echo "Opción desconocida: $1"; exit 1 ;;
    esac
    shift
done

IFS=',' read -ra SERVICE_LIST <<< "$SERVICES"

for SERVICE in "${SERVICE_LIST[@]}"; do
    echo "Deteniendo $SERVICE..."
    pkill -f "src/$SERVICE/app.py"
done
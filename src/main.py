# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: [nombre_del_archivo.py]
# Descripción: [breve descripción del propósito del archivo]
# ============================================================
import sys, os

def suma(a, b):
    return a + b
        
def resta(a, b):
    return a - b

def main():
    # Status: OK
    status = os.EX_OK

    try:
        resultado = suma(3, 5)
        print(f"Resultado: {resultado}\n")
    except Exception as e:
        # Status: Error de software
        status = os.EX_SOFTWARE
        print(f"Error inesperado: {e}\n")

    try:
        resultado = resta(3, 5)
        print(f"Resultado: {resultado}\n")
    except Exception as e:
        # Status: Error de software
        status = os.EX_SOFTWARE
        print(f"Error inesperado: {e}\n")

    # Return de la función: status EX_OK (0) | EX_SOFTWARE (70)
    return status 

if __name__ == "__main__":
    sys.exit(main())
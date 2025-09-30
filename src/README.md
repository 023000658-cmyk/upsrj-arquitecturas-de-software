# **Arquitectura de Microservicios con Flask**

# **Índice**
- [**Arquitectura de Microservicios con Flask**](#arquitectura-de-microservicios-con-flask)
- [**Índice**](#índice)
- [**Fecha de entrega**](#fecha-de-entrega)
- [**Descripción del Proyecto**](#descripción-del-proyecto)
- [**Resumen de Arquitectura**](#resumen-de-arquitectura)
- [**Patrones Utilizados**](#patrones-utilizados)
- [**Actividad de clase**](#actividad-de-clase)
  - [Objetivos](#objetivos)
  - [Pasos](#pasos)
- [**Tarea**](#tarea)
  - [Objetivos](#objetivos-1)
  - [Pasos](#pasos-1)
  - [Detalles](#detalles)
    - [Estructura del proyecto](#estructura-del-proyecto)
    - [Rutas del microservicio](#rutas-del-microservicio)
    - [Estructura de datos](#estructura-de-datos)
    - [Validación cruzada](#validación-cruzada)
    - [Actualización del Gateway](#actualización-del-gateway)
- [**Contacto**](#contacto)

---

# **Fecha de entrega**

- Fecha de inicio:  29/09/25
- Fecha de entrega: 08/10/25

🔙 [Volver al índice](#índice)

---

# **Descripción del Proyecto**

Este proyecto es una práctica de arquitectura de software basada en microservicios.
Incluye tres componentes principales:

- **Servicio de Usuarios:** gestiona los usuarios, ofreciendo endpoints para crear, listar y visualizar información de cada usuario.
- **Servicio de Productos:** gestiona los productos, proporcionando endpoints para crear, listar y consultar datos de productos.
- **Servicio Gateway:** actúa como punto de entrada unificado para consumir los datos de los otros servicios.

Cada microservicio se ejecuta de forma independiente con su propio servidor `Flask`, archivos locales de datos `(.json)` y plantillas `HTML` para las vistas.

🔙 [Volver al índice](#índice)

---

# **Resumen de Arquitectura**

- **Lenguaje:** Python 3 (framework Flask).
- **Arquitectura:** Microservicios con estilo RESTful.
- **Componentes principales:**
  - `users_services/`: servicio de gestión de usuarios.
  - `products_services/`: servicio de gestión de productos.
  - `gateway/`: orquestador y punto de acceso unificado.
- **Comunicación:** HTTP (peticiones entre microservicios vía Flask).
- **Datos:** persistencia en archivos locales JSON (users.json, products.json).
- **Front-end:** plantillas HTML renderizadas con Flask (Jinja2).
- **Despliegue:** ejecución local mediante scripts .sh (Linux/macOS) o .ps1 (Windows).


🔙 [Volver al índice](#índice)

---

# **Patrones Utilizados**

| Patrón                    | Propósito                                                                 |
|---------------------------|---------------------------------------------------------------------------|
| **Microservicios**        | Divide el sistema en servicios independientes y débilmente acoplados      |
| **Gateway**               | Proporciona un punto de entrada único para los clientes, ocultando la complejidad de los servicios |
| **Repositorio**           | Encapsula la lógica de acceso a datos utilizando archivos JSON como almacenamiento |
| **Inyección de Dependencias** | Desacopla los componentes y facilita las pruebas y extensiones de los servicios |
| **Modelo-Vista-Controlador** | Separa responsabilidades: rutas de Flask (controladores), plantillas (vistas) y datos JSON (modelos) |
| **API RESTful**           | Estandariza la comunicación entre servicios mediante métodos HTTP         |

🔙 [Volver al índice](#índice)

---

# **Actividad de clase**

## Objetivos

- Explora cómo interactúan los microservicios independientes dentro de la arquitectura.  
- Agrega nuevos **usuarios** y **productos**, luego verifica la consistencia de los datos a través del Gateway.  
- Observa cómo responde el sistema cuando uno de los microservicios no está disponible.  
- Identifica los mensajes de error o respuestas que devuelve el Gateway cuando un servicio está caído.  
- Reflexiona sobre la importancia de la **tolerancia a fallos** y la **resiliencia** en sistemas distribuidos.

## Pasos

1. **Inicia todos los microservicios** (Usuarios, Productos, Gateway).  
2. **Agrega usuarios** desde el servicio de Usuarios y verifica que aparezcan en el Gateway.  
3. **Agrega productos** desde el servicio de Productos y confirma que puedan consultarse desde el Gateway.  
4. **Detén uno de los microservicios** (por ejemplo, el servicio de Productos) e intenta acceder a los productos a través del Gateway.  
5. **Documenta tus observaciones**: qué respuestas se devuelven, qué sigue funcionando y qué falla.  
6. **Reinicia el servicio detenido** y verifica la recuperación del sistema.

🔙 [Volver al índice](#índice)

---

# **Tarea**

## Objetivos

- Comprende los principios del diseño basado en microservicios.  
- Configura un nuevo microservicio en Flask con rutas y plantillas.  
- Implementa un modelo de datos que permita a los **usuarios referenciar productos comprados**.  
- Establece comunicación entre el **Servicio de Usuarios** y el **Servicio de Productos**.  
- Practica la **persistencia de datos** utilizando archivos JSON (o un almacén simple equivalente).  
- Integra el nuevo microservicio con el **Servicio Gateway** para acceso unificado.  
- Prueba el flujo completo:  
  1. Crear usuarios  
  2. Crear productos  
  3. Asignar productos comprados a los usuarios  
  4. Consultar detalles del usuario incluyendo su lista de productos

## Pasos

1. **Configura la estructura del proyecto** para el nuevo microservicio `purchases_service/`.  
2. **Define las rutas** para:  
   - Crear una compra (enlazando un usuario con un producto).  
   - Listar las compras de un usuario.  
3. **Modifica el Servicio de Usuarios** para almacenar un campo `purchased_products` (lista de IDs de productos).  
4. **Conéctate con el Servicio de Productos** para validar la existencia del producto.  
5. **Actualiza el Gateway** para exponer endpoints combinados (usuarios + productos comprados).
6. **Actualiza el orquestador** para arrancar el microservicio nuevo (descomenta las líneas 24,25 de `run-all.sh`).
    ```bash
    ["Purchases Service"]="src/purchases_service/app.py"
    ["Purchases API"]="src/purchases_service/api.py"
    ```
7. **Actualiza el orquestador** para detener el microservicio nuevo (descomenta las líneas 19,20 de `stop-all.sh`).
    ```bash
    "purchases_service/api.py"
    "purchases_service/app.py"
    ```
8. **Prueba el flujo completo** con datos de ejemplo.

## Detalles 

### Estructura del proyecto

```bash
purchases_service/ 
├── app.py                  # Lógica principal del microservicio 
├── purchases.json          # Persistencia local de compras 
└── templates/ 
  ├── purchases.html        # Vista para listar compras por usuario    
  └── create_purchase.html  # Formulario para registrar una compra
```

### Rutas del microservicio


- `GET /purchases/<int:user_id>`  
  Lista todas las compras realizadas por el usuario con ID `user_id`.

- `POST /purchases`  
  Crea una nueva compra. Requiere los campos:
  ```json
  {
    "user_id": 1,
    "product_id": 3
  }
  ```

### Estructura de datos

- `purchases.json`
  ```json
  [
    {
      "id": 1,
      "user_id": 1,
      "product_id": 3,
      "timestamp": "2025-09-29T17:45:00"
    }
  ]
  ```

- `users.json` (modificado)
  ```json
  [
    {
      "id": 1,
      "name": "Ana",
      "purchased_products": [3, 5]
    }
  ]
  ```

### Validación cruzada

Antes de registrar una compra, el microservicio debe:

- Verificar que el `user_id` exista en `users_service` (`GET /api/users/<id>`)
- Verificar que el `product_id` exista en `products_service` (`GET /api/products/<id>`)

Si alguno no existe, debe devolver `400 Bad Request` con un mensaje claro.

### Actualización del Gateway

Nueva ruta combinada:
- `GET /api/users/<int:user_id>/purchases`

Devuelve los datos del usuario junto con los productos comprados.

Ejemplo de respuesta:
  ```json
  {
    "user": {
      "id": 1,
      "name": "Ana"
    },
    "purchased_products": [
      {
        "id": 3,
        "name": "Laptop"
      },
      {
        "id": 5,
        "name": "Mouse"
      }
    ]
  }
  ```

### Puertos para ejecución local

| Microservicio        | Archivo principal           | Puerto | Descripción breve                            |
|----------------------|-----------------------------|--------|----------------------------------------------|
| Gateway Web (opcional) | `gateway/app.py`          | 5000   | Interfaz web (si se implementa con templates)|
| Gateway API          | `gateway/api.py`            | 5001   | API unificada para frontend y consumo externo|
| Users Service        | `users_service/app.py`      | 5002   | Gestión de usuarios                          |
| Users API            | `users_service/api.py`      | 5003   | API para gestión de usuarios                 |
| Products Service     | `products_service/app.py`   | 5004   | Gestión de productos                         |
| Products API         | `products_service/api.py`   | 5005   | API para gestión de productos                |
| Purchases Service    | `purchases_service/app.py`  | 5006   | Registro y consulta de compras               |
| Purchases API        | `purchases_service/api.py`  | 5007   | API para registro y consulta de compras      |

🔙 [Volver al índice](#índice)

---

# **Contacto**

¿Dudas? Consulta los archivos de ayuda o pregunta a tu instructor.

**Autor:** Jesús Salvador López Ortega  
[LinkedIn](https://www.linkedin.com/in/jesus-salvador-lopez-ortega/) | [GitHub](https://github.com/chucholoport) | [Correo Institucional](mailto:jlopez@upsrj.edu.mx)

🔙 [Volver al índice](#índice)
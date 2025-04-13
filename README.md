# 🍕 Pizza Bella API - FastAPI + MongoDB

Este proyecto implementa una RESTful API para el sistema de gestión de pedidos, menús y reseñas de la cadena de restaurantes **Pizza Bella**, usando FastAPI y MongoDB.

---

## 📁 Estructura del Proyecto

```text
pizza_bella_api/
├── .env
├── .gitignore
├── README.md
├── requirements.txt
├── main.py
│
└── app/
    ├── __init__.py
    ├── config.py
    ├── db/
    │   ├── __init__.py
    │   └── client.py
    ├── models/
    │   ├── __init__.py
    │   ├── restaurant.py
    │   ├── user.py
    │   ├── menu_item.py
    │   ├── order.py
    │   └── review.py
    ├── schemas/
    │   ├── __init__.py
    │   ├── restaurant.py
    │   ├── user.py
    │   ├── menu_item.py
    │   ├── order.py
    │   └── review.py
    ├── controller/
    │   ├── __init__.py
    │   ├── restaurant.py
    │   ├── user.py
    │   ├── menu_item.py
    │   ├── order.py
    │   └── review.py
    ├── routes/
    │   ├── __init__.py
    │   ├── restaurant.py
    │   ├── user.py
    │   ├── menu_item.py
    │   ├── order.py
    │   └── review.py
    ├── test/
    │   ├── __init__.py
    │   ├── restaurants.py
    │   ├── users.py
    │   ├── menu_items.py
    │   ├── orders.py
    │   └── reviews.py
    └── utils/
        └── helpers.py
```

---

## 📄 Archivos raíz

- **`main.py`**  
  Punto de entrada principal de la aplicación FastAPI. Aquí se inicializa la app, se configuran los routers y se arranca el servidor.

- **`.env`**  
  Archivo para definir variables de entorno como la URL de conexión a MongoDB.

- **`requirements.txt`**  
  Lista de dependencias de Python para el entorno del proyecto.

- **`README.md`**  
  Este archivo de documentación.

---

## 📁 `app/` - Código fuente de la aplicación

### `config.py`  
Carga y gestiona variables de entorno, configuración del proyecto, etc.

---

### 📁 `db/`

- **`client.py`**  
  Contiene la conexión asincrónica a MongoDB usando `motor`.

---

### 📁 `models/`

Define las estructuras base que representan cada colección en MongoDB. Aunque MongoDB es schemaless, aquí se modelan como referencia.

- `restaurant.py` – Estructura base para restaurantes.  
- `user.py` – Modelo de usuarios.  
- `menu_item.py` – Ítems del menú (productos).  
- `order.py` – Pedidos realizados por los usuarios.  
- `review.py` – Reseñas de los usuarios para restaurantes/pedidos.

---

### 📁 `schemas/`

Esquemas de validación con **Pydantic** para datos de entrada (POST/PUT) y salida (GET).

- Cada archivo define los `Create`, `Update`, y `Response` schemas correspondientes.

---

### 📁 `controller/`

Contiene funciones para interactuar con la base de datos (MongoDB).

- Cada archivo implementa la lógica de acceso para su entidad correspondiente.

---

### 📁 `routes/`

Define los endpoints expuestos por la API REST.

- Aquí se registran las rutas y se conectan con la lógica `controller/` y los `schemas/`.

---

### 📁 `utils/`

Funciones auxiliares o utilitarias.

- `helpers.py` – Ejemplo: hashing de contraseñas, validación, manejo de fechas, etc.

---

### 📁 `test/`

Pruebas unitaria para endpoints.

- Aqui estaran las pruebas unitarias para saber como hacer peticiones al backend, ademas de confirmar su funcionalidad.

---

## 🚀 Cómo ejecutar

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor
uvicorn main:app --reload

# Ejecutar pruebas
pytest -s app\test\restaurants.py
```

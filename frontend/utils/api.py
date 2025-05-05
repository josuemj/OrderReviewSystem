import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("BACKEND_URI", "http://localhost:8000").rstrip("/")

"""
Login
"""

def authenticate_user(email: str, password: str):
    try:
        response = requests.post(
            f"{API_URL}/login",
            json={"email": email, "password": password}
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print("Error de conexión:", e)
        return None
    
def register_user(name: str, email: str, password: str):
    try:
        response = requests.post(
            f"{API_URL}/register",
            json={
                "name": name,
                "email": email,
                "password": password
            }
        )
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            # Captura el mensaje de error del backend
            return {
                "success": False,
                "detail": response.json().get("detail", "Error desconocido")
            }
    except Exception as e:
        return {"success": False, "detail": str(e)}

"""
Restaurants
"""
def create_restaurant(data: dict):
    try:
        response = requests.post(f"{API_URL}/restaurants/", json=data)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print("Error al crear restaurante:", e)
        return None

def update_restaurant(restaurant_id: str, data: dict):
    try:
        response = requests.put(f"{API_URL}/restaurants/{restaurant_id}", json=data)
        return response.status_code == 200
    except Exception as e:
        print("Error al actualizar restaurante:", e)
        return False

def get_restaurants_by_category(category: str):
    try:
        response = requests.get(f"{API_URL}/restaurants/by-category", params={"category": category})
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print("Error al buscar por categoría:", e)
        return []

def get_categories():
    try:
        response = requests.get(f"{API_URL}/restaurants/categories")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print("Error al buscar por categoría:", e)
        return []

def get_all_restaurants():
    try:
        response = requests.get(f"{API_URL}/restaurants/")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print("Error obteniendo restaurantes:", e)
        return []

def get_top_rated_restaurants(limit=10):
    try:
        response = requests.get(f"{API_URL}/restaurants/top-rated", params={"limit": limit})
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print("Error obteniendo mejores calificados:", e)
        return []
    
def get_avg_rating_by_restaurant(restaurant_id: str):
    try:
        response = requests.get(f"{API_URL}/restaurants/avg-rating", params={"id": restaurant_id})
        if response.status_code == 200 and response.json():
            return response.json()[0]  
        return None
    except Exception as e:
        print("Error al obtener rating promedio:", e)
        return None

def create_new_categories_to_restaurant(restaurant_id: str, categories: list):
    try:
        payload = {
            "restaurant_id": restaurant_id,
            "categories": categories
        }
        response = requests.post(f"{API_URL}/restaurants/categories", json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            print("Error al crear categorías:", response.status_code, response.text)
            return None
    except Exception as e:
        print("Error al conectar con la API:", e)
        return None

def remove_categories_from_restaurant(restaurant_id: str, categories: list):
    try:
        payload = {
            "restaurant_id": restaurant_id,
            "categories": categories
        }
        response = requests.delete(f"{API_URL}/restaurants/categories", json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            print("Error al eliminar categorías:", response.status_code, response.text)
            return None
    except Exception as e:
        print("Error al conectar con la API:", e)
        return None


"""
Reviews
"""

def get_all_reviews(page: int, limit: int = 10, user_id=None):
    try:
        params = {"page": page, "limit": limit}
        if user_id:
            params["user_id"] = user_id  

        response = requests.get(f"{API_URL}/reviews", params=params)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print("Error paginando reseñas:", e)
        return []


def create_review(data: dict):
    try:
        response = requests.post(f"{API_URL}/reviews/", json=data)
        return response.status_code == 200
    except Exception as e:
        print("Error al crear reseña:", e)
        return False

def update_review(review_id: str, data: dict):
    try:
        response = requests.put(f"{API_URL}/reviews/{review_id}", json=data)
        return response.status_code == 200
    except Exception as e:
        print("Error al actualizar reseña:", e)
        return False

def delete_review(review_id: str):
    try:
        response = requests.delete(f"{API_URL}/reviews/{review_id}")
        return response.status_code == 200
    except Exception as e:
        print("Error al eliminar reseña:", e)
        return False


"""
menu items
"""

def get_menu_items_by_restaurant(restaurant_id: str):
    try:
        response = requests.get(f"{API_URL}/menu-items/by-restaurant/{restaurant_id}")
        if response.status_code == 200: 
            return response.json()
        return []
    except Exception as e:
        print("Error obteniendo platillos del restaurante:", e)
        return []

def get_total_items():
    try:
        response = requests.get(f"{API_URL}/menu-items/total")
        if response.status_code == 200:
            return response.json().get("total", 0)
        else:
            print("Error al obtener total de órdenes:", response.status_code)
            return 0
    except Exception as e:
        print("Error al conectar con la API:", e)
        return 0
    
def get_top_selling_menu_items(top: int = 10):
    try:
        response = requests.get(f"{API_URL}/menu-items/top", params={"limit": top})  # <--- aquí cambio "top" por "limit"
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print("Error obteniendo platillos más vendidos:", e)
        return []

def get_all_menu_items():
    try:
        response = requests.get(f"{API_URL}/menu-items/all") 
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print("Error obteniendo todos los platillos:", e)
        return []

def create_menu_item(data, image_file):
    try:
        files = {
            'image': (image_file.name, image_file, 'multipart/form-data')
        }
        payload = {
            'restaurantId': data['restaurantId'],
            'name': data['name'],
            'description': data['description'],
            'price': str(data['price']),
        }
        response = requests.post(f"{API_URL}/menu-items/", data=payload, files=files)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error al crear platillo:", response.status_code, response.text)
            return None
    except Exception as e:
        print("Excepción al crear platillo:", e)
        return None
        
def get_menu_image(image_file_id: str):
    if image_file_id:
        return f"{API_URL}/menu-items/images/{image_file_id}"
    else:
        # Imagen por defecto si no hay `image_file_id`
        return "https://via.placeholder.com/400x300?text=Sin+imagen"

def delete_menu_item(menu_item_id):
    try:
        response = requests.delete(f"{API_URL}/menu-items/{menu_item_id}")
        return response.status_code == 200
    except Exception as e:
        print("Error al eliminar platillo:", e)
        return False

"""
orders
"""

def set_order(data: dict):
    try:
        response = requests.post(f"{API_URL}/orders/", json=data)
        return response.status_code == 200
    except Exception as e:
        print("Error al crear orden:", e)
        return False

def get_total_orders():
    try:
        response = requests.get(f"{API_URL}/orders/total")
        if response.status_code == 200:
            return response.json().get("total", 0)
        else:
            print("Error al obtener total de órdenes:", response.status_code)
            return 0
    except Exception as e:
        print("Error al conectar con la API:", e)
        return 0

def get_orders_by_user(userId: str):
    try:
        response = requests.get(f"{API_URL}/orders/user/{userId}")
        if response.status_code == 200:
            return response.json()  # Devuelve la lista de órdenes
        else:
            print("Error al obtener órdenes:", response.status_code)
            return []
    except Exception as e:
        print("Error al conectar con la API:", e)
        return []

def get_sorted_orders_by_user(user_id: str):
    try:
        response = requests.get(f"{API_URL}/orders/usersortorders/{user_id}")
        if response.status_code == 200:
            return response.json()
        else:
            print("Error al obtener órdenes ordenadas:", response.status_code)
            return []
    except Exception as e:
        print("Error al conectar con la API:", e)
        return []

def delete_order(order_id: str):
    try:
        response = requests.delete(f"{API_URL}/orders/{order_id}")
        return response.status_code == 200
    except Exception as e:
        print("Error al eliminar orden:", e)
        return False

def update_order(data: dict):
    try:
        response = requests.put(f"{API_URL}/orders/{data['orderId']}", json=data)
        return response.status_code == 200
    except Exception as e:
        print("Error al actualizar orden:", e)
        return False

def get_orders_by_user_and_date(user_id: str, start_date: str, end_date: str):
    try:
        params = {
            "user_id": user_id,
            "start_date": start_date,
            "end_date": end_date
        }
        response = requests.get(f"{API_URL}/orders/by-user-and-date", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error al obtener órdenes por rango de fechas:", response.status_code)
            return []
    except Exception as e:
        print("Error al conectar con la API:", e)
        return []




"""
Files (Upload and Download)
"""

def upload_file_to_collection(collection: str, filepath: str):
    try:
        with open(filepath, "rb") as f:
            files = {"file": (os.path.basename(filepath), f)}
            response = requests.post(f"{API_URL}/upload-file", params={"collection": collection}, files=files)
        if response.status_code == 200:
            return {"success": True, "output": response.json()}
        else:
            return {"success": False, "detail": response.json().get("detail", "Error desconocido")}
    except Exception as e:
        return {"success": False, "detail": str(e)}

def download_collection_file(collection: str, file_format: str):
    try:
        params = {"collection": collection, "format": file_format}
        response = requests.get(f"{API_URL}/download-files", params=params, stream=True)
        
        if response.status_code == 200:
            filename = response.headers.get("content-disposition", "").split("filename=")[-1].replace('"', '')
            if not filename:
                filename = f"{collection}.{file_format}"

            download_path = os.path.join("downloads", filename)
            os.makedirs(os.path.dirname(download_path), exist_ok=True)

            with open(download_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return {"success": True, "path": download_path}
        else:
            return {"success": False, "detail": response.json().get("detail", "Error desconocido")}
    except Exception as e:
        return {"success": False, "detail": str(e)}
    
"""
Users (admin)
"""
def get_all_users(page: int = 1, limit: int = 10):
    try:
        response = requests.get(f"{API_URL}/users", params={"page": page, "limit": limit})
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print("Error al obtener usuarios:", e)
        return []

def create_user(data: dict):
    try:
        response = requests.post(f"{API_URL}/users", json=data)
        return response.status_code == 200
    except Exception as e:
        print("Error al crear usuario:", e)
        return False

def update_user(user_id: str, data: dict):
    try:
        print("🚨 Payload enviado a PUT /users:", data)  # Añade esto
        response = requests.put(f"{API_URL}/users/{user_id}", json=data)
        print("💥 Respuesta:", response.status_code, response.text)  # Y esto
        return response.status_code == 200
    except Exception as e:
        print("Error al actualizar usuario:", e)
        return False

def delete_user(user_id: str):
    try:
        response = requests.delete(f"{API_URL}/users/{user_id}")
        return response.status_code == 200
    except Exception as e:
        print("Error al eliminar usuario:", e)
        return False
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("BACKEND_URI", "http://localhost:8000").rstrip("/")

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

def get_all_reviews(page: int, limit: int = 10):
    try:
        response = requests.get(f"{API_URL}/reviews", params={"page": page, "limit": limit})
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

def get_orders_by_user(userId : str):
    pass
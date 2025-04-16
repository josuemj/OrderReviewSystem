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

def get_all_restaurants():
    #TODO: R de restaurants
    pass


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

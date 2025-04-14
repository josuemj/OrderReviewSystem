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

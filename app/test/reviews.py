import sys
import os

# Añade explícitamente la raíz del proyecto (donde está main.py)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, ROOT_DIR)

from main import app

import pytest
from httpx import AsyncClient
from httpx import ASGITransport


@pytest.mark.asyncio
async def test_reviews_crud():
    transport = ASGITransport(app=app, raise_app_exceptions=True)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Crear
        review_data = {
            "userId": "67f84c4a4f94d86205b284d3",
            "restaurantId": "67f8598507801888ac0c0294",
            "orderId": "67f84d2281177535e8c7d9c7",
            "rating": 4.9,
            "comment": "¡Excelente todo!"
        }
        response = await client.post("/reviews/", json=review_data)
        assert response.status_code == 200
        review_id = response.json()
        print("CREATE: PASSED")

        # Leer
        response = await client.get(f"/reviews/{review_id}")
        assert response.status_code == 200
        assert response.json()["comment"] == "¡Excelente todo!"
        print("READ: PASSED")

        # Actualizar
        response = await client.put(f"/reviews/{review_id}", json={
            "comment": "Muy buena experiencia",
            "rating": 4.7
        })
        assert response.status_code == 200
        assert response.json()["message"] == "Actualizado correctamente"
        print("UPDATE: PASSED")

        # Confirmar cambio
        response = await client.get(f"/reviews/{review_id}")
        assert response.json()["comment"] == "Muy buena experiencia"

        # Eliminar
        response = await client.delete(f"/reviews/{review_id}")
        assert response.status_code == 200
        print("DELETE: PASSED")

        # Confirmar eliminación
        response = await client.get(f"/reviews/{review_id}")
        assert response.status_code == 404
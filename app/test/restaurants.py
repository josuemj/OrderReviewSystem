import sys
import os
import pytest
from httpx import AsyncClient, ASGITransport

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, ROOT_DIR)

from main import app


@pytest.mark.asyncio
async def test_reviews_crud():
    transport = ASGITransport(app=app, raise_app_exceptions=True)

    async with AsyncClient(transport=transport, base_url="http://test") as client:

        #TODO: CRUD Y DEMAS FUNCIONES FALTAN CON TEST

        # Obtener restaurantes mejor calificados
        response = await client.get("/restaurants/top-rated?limit=10")
        assert response.status_code == 200
        top_restaurants = response.json()
        assert isinstance(top_restaurants, list)
        assert all("averageRating" in r and "name" in r for r in top_restaurants)
        print("TOP RATED RESTAURANTS: PASSED")

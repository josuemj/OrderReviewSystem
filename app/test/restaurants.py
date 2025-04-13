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

        # Obtener promedio de calificación por restaurante
        response = await client.get("/restaurants/avg-rating")
        assert response.status_code == 200
        avg_reviews = response.json()
        assert isinstance(avg_reviews, list)
        assert all("averageRating" in r and "totalReviews" in r and "_id" in r for r in avg_reviews)
        print("AVG RATING PER RESTAURANT: PASSED")

        # Obtener promedio de calificación por restaurante con id específico
        restaurant_id = avg_reviews[0]["_id"]  # Tomamos uno válido del resultado anterior
        response = await client.get(f"/restaurants/avg-rating?id={restaurant_id}")
        assert response.status_code == 200
        single_avg = response.json()
        assert isinstance(single_avg, list)
        assert len(single_avg) == 1
        assert single_avg[0]["_id"] == restaurant_id
        assert "averageRating" in single_avg[0]
        assert "totalReviews" in single_avg[0]
        assert "name" in single_avg[0]
        print("AVG RATING BY ID: PASSED")

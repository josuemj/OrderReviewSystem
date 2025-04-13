import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, ROOT_DIR)

from main import app
import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status
from main import app

@pytest.mark.asyncio
async def test_download_files():
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://test") as client:

        formats = {
            "json": "application/json",
            "csv": ["text/csv", "application/vnd.ms-excel"],
            "bson": "application/octet-stream"
        }

        for fmt, expected in formats.items():
            response = await client.get("/download-files", params={"collection": "restaurants", "format": fmt})
            assert response.status_code == status.HTTP_200_OK

            content_type = response.headers["content-type"]
            if fmt == "csv":
                assert content_type in expected, f"Expected one of {expected}, got {content_type}"
            else:
                assert content_type == expected, f"Expected {expected}, got {content_type}"

            print(f"Download {fmt.upper()} successful with correct content-type.")

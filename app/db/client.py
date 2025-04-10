from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client: AsyncIOMotorClient = AsyncIOMotorClient(settings.mongodb_uri)
db = client.get_default_database()  # Usará el nombre de la DB que esté en el URI
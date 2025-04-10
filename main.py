from fastapi import FastAPI
from app.db.client import client

app = FastAPI()

@app.on_event("startup")
async def startup_db_check():
    try:
        await client.admin.command("ping")
        print("✅ Conexión a MongoDB Atlas exitosa.")
    except Exception as e:
        print("❌ Error de conexión a MongoDB:", e)

@app.get("/")
async def root():
    return {"message": "Pizza Bella API en línea"}

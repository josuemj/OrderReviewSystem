from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pymongo.errors import PyMongoError
from app.db.client import client
from app.routes import review, restaurant

app = FastAPI()
app.include_router(review.router)
app.include_router(restaurant.router)

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

@app.get("/healthcheck", tags=["Health"])
async def healthcheck():
    try:
        await client.admin.command("ping")
        return JSONResponse(status_code=200, content={"status": "ok", "db": "connected"})
    except PyMongoError as e:
        return JSONResponse(status_code=500, content={"status": "error", "db": "disconnected", "detail": str(e)})
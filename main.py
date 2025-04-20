from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pymongo.errors import PyMongoError
from app.db.client import client
from app.routes import review, restaurant, files, login, menu_item, order
from dotenv import load_dotenv
from contextlib import asynccontextmanager

load_dotenv()

# start up logic
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await client.admin.command("ping")
        print("✅ Conexión a MongoDB Atlas exitosa.")
    except Exception as e:
        print("❌ Error de conexión a MongoDB:", e)

    yield  
    print("App shutting down... (you can clean resources here)")

app = FastAPI(lifespan=lifespan)

app.include_router(review.router)
app.include_router(restaurant.router)
app.include_router(files.router)
app.include_router(login.router)
app.include_router(menu_item.router)
app.include_router(order.router)


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
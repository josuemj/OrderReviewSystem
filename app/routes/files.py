from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import subprocess
import os

router = APIRouter()

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = "pizzabella"

@router.post("/upload-file")
async def upload_file(collection: str, file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1].lower()
    if ext not in ["json", "csv", "bson"]:
        raise HTTPException(status_code=400, detail="Formato no soportado. Usa .json, .csv o .bson")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as temp:
            content = await file.read()
            temp.write(content)
            temp.flush()

            command = [
                "mongoimport",
                f"--uri={MONGO_URI}",
                f"--db={DB_NAME}",
                f"--collection={collection}",
                f"--file={temp.name}"
            ]

            if ext == "csv":
                command.append("--type=csv")
                command.append("--headerline")
            elif ext == "json":
                command.append("--jsonArray")

            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            os.unlink(temp.name)  # Eliminar archivo temporal

            if result.returncode != 0:
                raise HTTPException(status_code=500, detail=f"mongoimport error: {result.stderr}")

            return JSONResponse(content={"message": "Importación completada", "output": result.stdout})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

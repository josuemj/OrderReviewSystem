from fastapi import Query, APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
import tempfile
import subprocess
import os

router = APIRouter()
EXPORT_DIR = "exports"

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

@router.get("/download-files")
def download_collection(
    collection: str = Query(..., description="Nombre de la colección a exportar"),
    format: str = Query(..., pattern="^(json|csv|bson)$", description="Formato: json, csv, bson")
):
    export_path = os.path.join(EXPORT_DIR, f"{collection}.{format}")

    # Borrar archivo si ya existe
    if os.path.exists(export_path):
        os.remove(export_path)

    uri = os.getenv("MONGODB_URI")

    if not uri or not uri.startswith("mongodb"):
        raise HTTPException(status_code=500, detail=f"URI inválida: {uri}")

    if format == "bson":
        export_path = os.path.join(EXPORT_DIR, "pizzabella", f"{collection}.bson")
        dump_path = os.path.join(EXPORT_DIR)

        command = [
            "mongodump",
            f"--uri={uri}",
            f"--collection={collection}",
            f"--out={dump_path}",
        ]
    else:
        command = [
            "mongoexport",
            f"--uri={uri}",
            f"--collection={collection}",
            f"--out={export_path}",
        ]
        if format == "csv":
            command.extend(["--type=csv", "--fields=_id"])

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        raise HTTPException(status_code=500, detail="Error al exportar la colección")

    return FileResponse(
        export_path,
        filename=os.path.basename(export_path),
        media_type="application/octet-stream" if format == "bson" else None
    )
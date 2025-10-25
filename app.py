from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from typing import Optional
import subprocess
import os
import shutil

app = FastAPI(title="ReMarkable API wrapper")

DATA_DIR = "/data"

@app.on_event("startup")
def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def run_rmapi(args):
    """Запуск rmapi внутри контейнера"""
    try:
        cmd = ["docker", "exec", "rmapi", "rmapi"] + args
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60
        )
        return {
            "success": result.returncode == 0,
            "output": result.stdout.strip(),
            "error": result.stderr.strip() if result.returncode != 0 else None
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/")
def root():
    return {"status": "ok", "message": "ReMarkable API wrapper"}

@app.post("/put")
async def put_file(
    file: UploadFile = File(...),
    folder: Optional[str] = Form("/")
):
    """Загрузить файл в ReMarkable"""
    try:
        # Сохраняем файл
        target_path = os.path.join(DATA_DIR, file.filename)
        
        with open(target_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Загружаем в reMarkable
        result = run_rmapi(["put", target_path, folder])
        
        # Удаляем временный файл
        if os.path.exists(target_path):
            os.remove(target_path)
        
        return {
            "success": True,
            "filename": file.filename,
            "folder": folder,
            "rmapi_result": result
        }
        
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

@app.get("/ls")
def list_files(path: str = "/"):
    """Список файлов на ReMarkable"""
    return run_rmapi(["ls", path])

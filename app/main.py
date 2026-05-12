from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from typing import List, Dict, Any

from app.schemas import MeasurementCreate, Measurement
from app.database import db

app = FastAPI(
    title="Neurostate",
    description="Cognitive Tracking System - Academic Module",
    version="1.0.0"
)

# Разрешение CORS для обеспечения гибкости при тестировании (включая мобильные устройства)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем папку со статичными файлами (стили, скрипты)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Указываем папку, где лежит index.html
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def serve_dashboard(request: Request):
    """Главная страница панели мониторинга."""
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/api/status", response_model=Dict[str, Any])
def get_system_status() -> Dict[str, Any]:
    """Возвращает текущий статус системы и рассчитанный день."""
    return {
        "system": "Neurostate",
        "status": "Operational",
        "current_day": db.get_current_day(),
        "measurements_count": len(db.measurements)
    }

@app.post("/api/measurements/", response_model=Measurement, status_code=201)
def create_measurement(payload: MeasurementCreate) -> Dict[str, Any]:
    """Создает новый замер в системе."""
    try:
        record = db.add_measurement(level=payload.level, notes=payload.notes)
        return record
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/measurements/", response_model=List[Measurement])
def get_measurements() -> List[Dict[str, Any]]:
    """Возвращает архив всех записей."""
    return db.measurements

@app.get("/api/statistics/", response_model=Dict[str, Any])
def get_statistics() -> Dict[str, Any]:
    """Возвращает агрегированные данные мониторинга."""
    return db.get_statistics()

@app.delete("/api/measurements/", response_model=Dict[str, Any])
def clear_measurements() -> Dict[str, Any]:
    """Очищает базу данных."""
    db.clear_all()
    return {"message": "Data cleared successfully."}
    

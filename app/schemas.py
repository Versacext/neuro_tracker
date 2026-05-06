# app/schemas.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MeasurementCreate(BaseModel):
    level: int = Field(..., ge=1, le=8, description="Уровень напряжения (от 1 до 8)", example=4)
    notes: Optional[str] = Field(None, description="Дополнительные комментарии или вердикт системы", example="Состояние в норме")

class Measurement(BaseModel):
    id: int
    day: int = Field(..., description="Автоматически рассчитанный день от точки старта")
    level: int = Field(..., ge=1, le=8)
    timestamp: str = Field(..., description="Временная метка в формате UTC ISO 8601")
    notes: Optional[str] = None
    system_verdict: Optional[str] = Field(None, description="Вердикт системы")

    class Config:
        from_attributes = True
      

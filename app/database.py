# app/database.py

from datetime import datetime
from typing import List, Dict, Any, Optional

class Database:
    def __init__(self):
        self.measurements: List[Dict[str, Any]] = []
        # Базовая точка отсчета из настроек системы
        self.start_time: datetime = datetime(2026, 4, 28, 12, 28)

    def get_current_day(self, current_time: Optional[datetime] = None) -> int:
        """Автоматический расчет дня от точки старта."""
        if current_time is None:
            current_time = datetime.utcnow()
        delta = current_time - self.start_time
        return max(1, delta.days + 1)

    def add_measurement(self, level: int, notes: Optional[str] = None) -> Dict[str, Any]:
        """Добавление нового замера с автоматическим расчетом дня и вердикта."""
        now = datetime.utcnow()
        day_number = self.get_current_day(now)
        record_id = len(self.measurements) + 1
        
        # Научно-ориентированный вердикт
        verdict = "Оптимальное когнитивное состояние" if level <= 4 else "Повышенное напряжение, рекомендуется отдых"

        record = {
            "id": record_id,
            "day": day_number,
            "level": level,
            "timestamp": now.isoformat(),
            "notes": notes,
            "system_verdict": verdict
        }
        
        self.measurements.append(record)
        return record

    def get_statistics(self) -> Dict[str, Any]:
        """Расчет показателей для панели мониторинга."""
        if not self.measurements:
            return {
                "current_level": None,
                "average_level": 0,
                "max_level": 0,
                "total_measurements": 0
            }
        
        levels = [m["level"] for m in self.measurements]
        return {
            "current_level": levels[-1],
            "average_level": round(sum(levels) / len(levels), 2),
            "max_level": max(levels),
            "total_measurements": len(self.measurements)
        }

    def clear_all(self):
        """Очистка базы данных."""
        self.measurements.clear()

db = Database()

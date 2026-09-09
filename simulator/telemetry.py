from dataclasses import dataclass
from datetime import datetime, timezone


# ช่วยสร้างรูปแบบสำหรับเก็บข้อมูลหนึ่งชุด โดยไม่ต้องเขียนส่วนประกอบพื้นฐานซ้ำเอง
@dataclass
class Telemetry:
    # ข้อมูลทุกชุดจะบอกว่าอุปกรณ์ใดส่งมา ค่าที่วัดได้เท่าไร และวัดเมื่อใด
    device_id: str
    temperature: float
    humidity: float
    timestamp: str

    @classmethod
    def create(
        cls,
        device_id: str,
        temperature: float,
        humidity: float,
    ):
        # สร้างข้อมูลชุดใหม่พร้อมบันทึกเวลาปัจจุบันตามเวลาสากล (UTC)
        return cls(
            device_id=device_id,
            temperature=temperature,
            humidity=humidity,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

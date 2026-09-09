import random

from sensors.base import BaseSensor

# ตัววัดอุณหภูมิจำลอง ใช้รูปแบบพื้นฐานร่วมกับตัววัดชนิดอื่น
class TemperatureSensor(BaseSensor):
    def __init__(self):
        # กำหนดชื่อของค่าที่วัดและหน่วยองศาเซลเซียส
        super().__init__(
            name="temperature",
            unit="°C",
        )
        
    def read(self) -> float:
        # สุ่มค่าเพื่อเลียนแบบอุณหภูมิที่เปลี่ยนแปลงอยู่ระหว่าง 25 ถึง 35 องศาเซลเซียส
        value = random.uniform(25.0, 35.0)
        
        # ปัดค่าให้เหลือทศนิยม 2 ตำแหน่งก่อนส่งกลับ
        return round(value, 2)

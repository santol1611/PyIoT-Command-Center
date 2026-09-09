from abc import ABC, abstractmethod

# เป็นรูปแบบพื้นฐานที่ตัววัดทุกชนิดใช้ร่วมกัน
class BaseSensor(ABC):
    def __init__(self, name: str, unit: str):
        # เก็บชื่อของสิ่งที่วัดและหน่วยที่ใช้แสดงผล
        self.name = name
        self.unit = unit
        
    # บังคับให้ตัววัดแต่ละชนิดกำหนดวิธีสร้างหรืออ่านค่าของตัวเอง
    @abstractmethod
    def read(self) -> float:
        """อ่านค่าแล้วส่งตัวเลขที่ได้กลับไปให้ส่วนอื่นใช้งาน"""
        pass

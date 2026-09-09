import random

from sensors.base import BaseSensor

# ตัววัดความชื้นจำลอง ใช้รูปแบบพื้นฐานร่วมกับตัววัดชนิดอื่น
class HumiditySensor(BaseSensor):
    def __init__(self):
        # กำหนดชื่อของค่าที่วัดและหน่วยเปอร์เซ็นต์
        super().__init__(
            name="humidity",
            unit="%",
        )

    def read(self) -> float:
        # สุ่มค่าเพื่อเลียนแบบความชื้นที่เปลี่ยนแปลงอยู่ระหว่าง 40 ถึง 80 เปอร์เซ็นต์
        value = random.uniform(40.0, 80.0)

        # ปัดค่าให้เหลือทศนิยม 2 ตำแหน่งก่อนส่งกลับ
        return round(value, 2)

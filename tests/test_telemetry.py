# เครื่องมือทดสอบที่มีอยู่ใน Python ใช้ตรวจว่าผลลัพธ์ตรงตามที่คาดหรือไม่
import unittest
# datetime ใช้อ่านข้อความเวลา; timedelta ใช้แทนระยะห่างจากเวลาสากล
from datetime import datetime, timedelta

# นำรูปแบบข้อมูลที่อุปกรณ์ส่งออกมาเป็นสิ่งที่จะทดสอบ
from simulator.telemetry import Telemetry


# รวม Test ของข้อมูล Telemetry; unittest.TestCase มีคำสั่ง assert สำหรับตรวจผล
class TestTelemetry(unittest.TestCase):
    # ชื่อที่ขึ้นต้นด้วย test_ ทำให้ unittest ค้นพบและรัน Test นี้เอง
    def test_timestamp_is_valid_utc_time(self):
        # สร้างข้อมูลตัวอย่างโดยใช้ค่าที่รู้ล่วงหน้า เพื่อมุ่งตรวจเรื่องเวลา
        telemetry = Telemetry.create(
            device_id="ESP32-ROOM-001",
            temperature=30.0,
            humidity=60.0,
        )

        # แปลงข้อความเวลากลับเป็นข้อมูลเวลา; ถ้ารูปแบบผิด Test จะหยุดพร้อมข้อผิดพลาด
        recorded_time = datetime.fromisoformat(telemetry.timestamp)

        # เวลา UTC ต้องมีส่วนต่างจากเวลาสากลเป็นศูนย์
        # ถ้าไม่มีข้อมูลเขตเวลาหรือส่วนต่างไม่ใช่ศูนย์ การตรวจนี้จะไม่ผ่าน
        self.assertEqual(recorded_time.utcoffset(), timedelta(0))
        
    def test_create_keeps_device_and_sensor_values(self):
        # สร้างข้อมูลด้วยค่าที่กำหนดไว้ เพื่อเช็กว่าโปรแกรมไม่ทำค่าหายหรือสลับช่อง
        telemetry = Telemetry.create(
            device_id="ESP32-ROOM-007",
            temperature=28.5,
            humidity=62.0,
        )

        # รหัสอุปกรณ์ต้องตรงกับรหัสที่ส่งเข้าไป
        self.assertEqual(telemetry.device_id, "ESP32-ROOM-007")
        # ค่าอุณหภูมิต้องถูกเก็บไว้ในช่องอุณหภูมิ
        self.assertEqual(telemetry.temperature, 28.5)
        # ค่าความชื้นต้องถูกเก็บไว้ในช่องความชื้น
        self.assertEqual(telemetry.humidity, 62.0)

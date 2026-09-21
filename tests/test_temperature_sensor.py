# ใช้บอก Python ว่าควรค้นหาไฟล์โค้ดจากโฟลเดอร์ใดบ้าง
import sys
# เครื่องมือทดสอบที่มีอยู่ใน Python ใช้ตรวจว่าผลลัพธ์ตรงตามที่คาดหรือไม่
import unittest
# ช่วยหาตำแหน่งไฟล์และโฟลเดอร์ โดยไม่ต้องเขียนที่อยู่แบบตายตัว
from pathlib import Path
# ใช้กำหนดค่าที่ปกติจะถูกสุ่มให้แน่นอน เฉพาะระหว่างการทดสอบ
from unittest.mock import patch

# เริ่มจากที่อยู่เต็มของไฟล์นี้ ย้อนขึ้นไปยังโฟลเดอร์หลัก แล้วชี้ไปที่ simulator
simulator_path = Path(__file__).resolve().parents[1] / "simulator"
# เพิ่มโฟลเดอร์นี้ไว้ในที่ค้นหา เพื่อให้โค้ด Sensor หาไฟล์ที่ต้องใช้ร่วมกันเจอ
sys.path.insert(0, str(simulator_path))

# นำตัววัดอุณหภูมิจำลองมาเป็นสิ่งที่จะทดสอบ
from simulator.sensors.temperature import TemperatureSensor

# รวม Test ของตัววัดอุณหภูมิ; unittest.TestCase มีคำสั่ง assert สำหรับตรวจผล
class TestTemperatureSensor(unittest.TestCase):
    # ชื่อที่ขึ้นต้นด้วย test_ ทำให้ unittest ค้นพบและรัน Test นี้เอง
    def test_temperature_is_within_expected_range(self):
        # สร้างตัววัด แล้วอ่านอุณหภูมิจำลองหนึ่งค่า
        sensor = TemperatureSensor()
        temperature = sensor.read()

        # ค่าที่อ่านได้ต้องไม่น้อยกว่า 25 องศาเซลเซียส
        self.assertGreaterEqual(temperature, 25.0)
        # และต้องไม่มากกว่า 35 องศาเซลเซียส
        self.assertLessEqual(temperature, 35.0)
        
    def test_temperature_sensor_has_correct_name_and_unit(self):
        # สร้างตัววัดเพื่อตรวจข้อมูลประจำตัว ไม่ต้องอ่านค่าสุ่ม
        sensor = TemperatureSensor()

        # ชื่อต้องบอกว่าเป็นอุณหภูมิ
        self.assertEqual(sensor.name, "temperature")
        # หน่วยต้องเป็นองศาเซลเซียส
        self.assertEqual(sensor.unit, "°C")
        
    def test_temperature_is_rounded_to_two_decimal_places(self):
        # เตรียมตัววัดสำหรับตรวจการปัดเศษ
        sensor = TemperatureSensor()

        # แทนการสุ่มชั่วคราวด้วย 27.456 เพื่อให้รู้ผลที่ควรได้แน่นอน
        # เมื่อออกจาก with การสุ่มจะกลับไปทำงานตามปกติ
        with patch(
            "simulator.sensors.temperature.random.uniform",
            return_value=27.456,
        ):
            # อ่านค่าขณะที่กำหนดผลการสุ่มไว้
            temperature = sensor.read()

        # ถ้าปัดทศนิยมเหลือ 2 ตำแหน่ง ผลต้องเป็น 27.46
        self.assertEqual(temperature, 27.46)

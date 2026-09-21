# ใช้บอก Python ว่าควรค้นหาไฟล์โค้ดจากโฟลเดอร์ใดบ้าง
import sys
# เครื่องมือทดสอบที่มีอยู่ใน Python ใช้ตรวจว่าผลลัพธ์ตรงตามที่คาดหรือไม่
import unittest
# ช่วยหาตำแหน่งไฟล์และโฟลเดอร์ โดยไม่ต้องเขียนที่อยู่แบบตายตัว
from pathlib import Path

# __file__ คือไฟล์ทดสอบนี้; resolve() หาที่อยู่เต็มของไฟล์
# parents[1] ย้อนขึ้นไปถึงโฟลเดอร์หลัก แล้ว / "simulator" ชี้ไปยังโฟลเดอร์โค้ด
simulator_path = Path(__file__).resolve().parents[1] / "simulator"
# str() เปลี่ยนที่อยู่เป็นข้อความ และ insert(0, ...) ให้ Python ค้นหาโฟลเดอร์นี้ก่อน
# จึงช่วยให้ device.py หาไฟล์ sensors และ telemetry ที่อยู่ใน simulator เจอ
sys.path.insert(0, str(simulator_path))

# นำอุปกรณ์จำลองมาใช้เป็นสิ่งที่เราจะทดสอบ
from simulator.device import VirtualDevice

# รวมการทดสอบอุปกรณ์จำลองไว้ด้วยกัน; unittest.TestCase มีคำสั่ง assert สำหรับตรวจผล
class TestVirtualDevice(unittest.TestCase):
    # ชื่อที่ขึ้นต้นด้วย test_ ทำให้ unittest ค้นพบและรันการทดสอบนี้เอง
    def test_device_has_correct_device_id(self):
        # สร้างอุปกรณ์ด้วยรหัสที่เรารู้ล่วงหน้า เพื่อจะได้ตรวจกลับได้
        device = VirtualDevice(device_id="ESP32-ROOM-001")

        # ตรวจว่ารหัสที่อุปกรณ์เก็บไว้ตรงกับรหัสที่กำหนดตอนสร้าง
        self.assertEqual(device.device_id, "ESP32-ROOM-001")
    
    # ตรวจว่าอุปกรณ์อ่านค่าจากตัววัดและรวมเป็นข้อมูลหนึ่งชุดได้
    def test_device_collects_telemetry(self):
        # เตรียมอุปกรณ์ที่จะใช้ในการทดสอบครั้งนี้
        device = VirtualDevice(device_id="ESP32-ROOM-001")
        # สั่งให้อุปกรณ์อ่านอุณหภูมิและความชื้น แล้วเก็บผลไว้ใน telemetry
        telemetry = device.collect_telemetry()

        # ข้อมูลชุดนี้ต้องระบุว่าเป็นของอุปกรณ์ที่เพิ่งสร้าง
        self.assertEqual(telemetry.device_id, "ESP32-ROOM-001")
        # GreaterEqual ตรวจว่าอุณหภูมิมากกว่าหรือเท่ากับ 25
        self.assertGreaterEqual(telemetry.temperature, 25.0)
        # LessEqual ตรวจว่าอุณหภูมิน้อยกว่าหรือเท่ากับ 35
        self.assertLessEqual(telemetry.temperature, 35.0)
        # ตรวจว่าความชื้นมากกว่าหรือเท่ากับ 40 เปอร์เซ็นต์
        self.assertGreaterEqual(telemetry.humidity, 40.0)
        # ตรวจว่าความชื้นน้อยกว่าหรือเท่ากับ 80 เปอร์เซ็นต์
        self.assertLessEqual(telemetry.humidity, 80.0)
        # ต้องมีเวลาบันทึกข้อมูล; ข้อนี้ตรวจแค่ว่าไม่ว่าง ไม่ได้ตรวจรูปแบบเวลา
        self.assertTrue(telemetry.timestamp)

# ใช้กำหนดตำแหน่งที่ Python จะค้นหาไฟล์ของ Simulator
import sys

# เครื่องมือทดสอบที่มีมาให้พร้อมกับ Python
import unittest

# ช่วยหาตำแหน่งโฟลเดอร์โดยไม่เขียน Path แบบตายตัว
from pathlib import Path

# MagicMock ใช้สร้าง Publisher จำลอง
# patch ใช้เปลี่ยนของจริงเป็นของจำลองเฉพาะระหว่าง Test
from unittest.mock import MagicMock, patch


# หาโฟลเดอร์ simulator จากตำแหน่งของไฟล์ Test นี้
simulator_path = Path(__file__).resolve().parents[1] / "simulator"

# เพิ่มโฟลเดอร์ simulator ให้ Python ค้นหา device.py ได้
sys.path.insert(0, str(simulator_path))


# นำ main.py มาเป็นสิ่งที่เราจะทดสอบ
from simulator import main as simulator_main


# รวม Test ที่เกี่ยวข้องกับการเริ่มและหยุด Simulator
class TestSimulatorMain(unittest.TestCase):
    # เปลี่ยน MqttPublisher ใน main.py ให้เป็นของจำลองระหว่าง Test นี้
    @patch("simulator.main.MqttPublisher")
    def test_main_stops_when_broker_connection_fails(
        self,
        mqtt_publisher_class,
    ):
        # สร้าง Publisher จำลองพร้อมที่อยู่ที่ main.py ใช้งาน
        publisher = MagicMock()
        publisher.host = "127.0.0.1"
        publisher.port = 1883

        # กำหนดว่าเมื่อเรียก connect() ให้จำลองเหตุการณ์เชื่อมต่อไม่ได้
        publisher.connect.side_effect = ConnectionRefusedError(
            "Connection refused"
        )

        # เมื่อ main.py สร้าง MqttPublisher ให้ส่ง Publisher จำลองนี้กลับไป
        mqtt_publisher_class.return_value = publisher

        # เปลี่ยน print() เป็นของจำลอง เพื่อเก็บข้อความไว้ตรวจสอบ
        with patch("builtins.print") as print_mock:
            simulator_main.main()

        # ตรวจว่า main.py พยายามเชื่อมต่อหนึ่งครั้ง
        publisher.connect.assert_called_once_with()

        # เมื่อเชื่อมต่อไม่สำเร็จ ต้องไม่พยายามส่ง Telemetry
        publisher.publish_telemetry.assert_not_called()

        # ตรวจว่าข้อความที่แสดงอธิบายปัญหาและตำแหน่ง Broker ครบ
        print_mock.assert_called_once_with(
            "ไม่สามารถเชื่อมต่อ MQTT Broker ได้\n"
            "ที่อยู่: 127.0.0.1:1883\n"
            "รายละเอียด: Connection refused"
        )

    # ตรวจว่า Simulator รอแล้วลองส่งใหม่ เมื่อ MQTT ส่งไม่สำเร็จ
    @patch("simulator.main.time.sleep")
    @patch("simulator.main.MqttPublisher")
    def test_main_retries_after_publish_timeout(
        self,
        mqtt_publisher_class,
        sleep_mock,
    ):
        # สร้าง Publisher จำลองและให้การเชื่อมต่อครั้งแรกสำเร็จ
        publisher = MagicMock()
        mqtt_publisher_class.return_value = publisher

        # การส่งครั้งแรกเกิด TimeoutError
        # การส่งครั้งที่สองจำลองว่าผู้ใช้กด Ctrl+C เพื่อจบ Test
        publisher.publish_telemetry.side_effect = [
            TimeoutError("Publish timed out"),
            KeyboardInterrupt(),
        ]

        # เก็บข้อความจาก print() ไว้ตรวจสอบโดยไม่แสดงบนหน้าจอ
        with patch("builtins.print") as print_mock:
            simulator_main.main()

        # ต้องพยายามส่งสองครั้ง แสดงว่ามีการเริ่มรอบใหม่
        self.assertEqual(
            publisher.publish_telemetry.call_count,
            2,
        )

        # หลังส่งไม่สำเร็จ ต้องรอ 2 วินาทีก่อนลองรอบถัดไป
        sleep_mock.assert_called_once_with(2)

        # เมื่อจบการทำงาน ต้องปิด MQTT เสมอ
        publisher.disconnect.assert_called_once_with()

        # ตรวจว่าผู้ใช้ได้รับข้อความอธิบายปัญหา
        print_mock.assert_any_call(
            "\nส่งข้อมูล MQTT ไม่สำเร็จ "
            "กำลังรอ 2 วินาทีก่อนลองใหม่\n"
            "รายละเอียด: Publish timed out"
        )

        # ตรวจว่าการกด Ctrl+C ได้รับการจัดการอย่างเรียบร้อย
        print_mock.assert_any_call(
            "\nหยุดการทำงานของ Simulator"
        )

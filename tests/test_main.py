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
    # ล้าง Environment Variables ชั่วคราว เพื่อทดสอบค่าเริ่มต้น
    @patch.dict(
        "simulator.main.os.environ",
        {},
        clear=True,
    )
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

        mqtt_publisher_class.assert_called_once_with(
            host="127.0.0.1",
            port=1883,
            username=None,
            password=None,
        )

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

    # ตรวจว่า Simulator ใช้ Host และ Port จาก Environment Variables
    @patch.dict(
        "simulator.main.os.environ",
        {
            "MQTT_HOST": "192.168.1.50",
            "MQTT_PORT": "1884",
        },
        clear=True,
    )
    @patch("simulator.main.MqttPublisher")
    def test_main_uses_mqtt_environment_settings(
        self,
        mqtt_publisher_class,
    ):
        # สร้าง Publisher จำลองเพื่อไม่เชื่อมต่อเครือข่ายจริง
        publisher = MagicMock()
        publisher.host = "192.168.1.50"
        publisher.port = 1884
        publisher.connect.side_effect = ConnectionRefusedError(
            "Connection refused"
        )
        mqtt_publisher_class.return_value = publisher

        # ซ่อนข้อความ Error เพราะ Test นี้มุ่งตรวจค่าที่ใช้สร้าง Publisher
        with patch("builtins.print"):
            simulator_main.main()

        # Host ต้องเป็นข้อความตามที่กำหนด
        # Port ต้องถูกแปลงจากข้อความ "1884" เป็นตัวเลข 1884
        mqtt_publisher_class.assert_called_once_with(
            host="192.168.1.50",
            port=1884,
            username=None,
            password=None,
        )

    # ตรวจว่า Simulator ส่ง Username และ Password ให้ MqttPublisher
    @patch.dict(
        "simulator.main.os.environ",
        {
            "MQTT_HOST": "127.0.0.1",
            "MQTT_PORT": "1883",
            "MQTT_USERNAME": "simulator",
            "MQTT_PASSWORD": "test-password",
        },
        clear=True,
    )
    @patch("simulator.main.MqttPublisher")
    def test_main_uses_mqtt_username_and_password(
        self,
        mqtt_publisher_class,
    ):
        # สร้าง Publisher จำลองและหยุดหลังขั้นเชื่อมต่อ
        publisher = MagicMock()
        publisher.host = "127.0.0.1"
        publisher.port = 1883
        publisher.connect.side_effect = ConnectionRefusedError(
            "Connection refused"
        )
        mqtt_publisher_class.return_value = publisher

        # ซ่อนข้อความเชื่อมต่อไม่สำเร็จ เพราะ Test นี้ตรวจ Credential
        with patch("builtins.print"):
            simulator_main.main()

        # ตรวจว่าข้อมูลยืนยันตัวตนถูกส่งครบ
        mqtt_publisher_class.assert_called_once_with(
            host="127.0.0.1",
            port=1883,
            username="simulator",
            password="test-password",
        )

    # ตรวจว่า Simulator ปฏิเสธ MQTT_PORT ที่อยู่นอกช่วง
    @patch.dict(
        "simulator.main.os.environ",
        {
            "MQTT_PORT": "70000",
        },
        clear=True,
    )
    @patch("simulator.main.MqttPublisher")
    def test_main_rejects_mqtt_port_outside_valid_range(
        self,
        mqtt_publisher_class,
    ):
        # เก็บข้อความที่โปรแกรมแสดงไว้ตรวจสอบ
        with patch("builtins.print") as print_mock:
            simulator_main.main()

        # Port ไม่ถูกต้อง จึงต้องยังไม่สร้าง Publisher
        mqtt_publisher_class.assert_not_called()

        # แจ้งช่วง Port ที่สามารถใช้งานได้
        print_mock.assert_called_once_with(
            "ค่า MQTT_PORT ไม่ถูกต้อง: 70000\n"
            "MQTT_PORT ต้องอยู่ระหว่าง 1 ถึง 65535"
        )

    # ตรวจว่า Simulator ปฏิเสธ MQTT_PORT ที่ไม่ใช่ตัวเลข
    @patch.dict(
        "simulator.main.os.environ",
        {
            "MQTT_PORT": "not-a-number",
        },
        clear=True,
    )
    @patch("simulator.main.MqttPublisher")
    def test_main_rejects_non_numeric_mqtt_port(
        self,
        mqtt_publisher_class,
    ):
        # เก็บข้อความที่โปรแกรมแสดงไว้ตรวจสอบ
        with patch("builtins.print") as print_mock:
            simulator_main.main()

        # ค่าผิดตั้งแต่ขั้นเตรียม จึงต้องยังไม่สร้าง Publisher
        mqtt_publisher_class.assert_not_called()

        # ข้อความต้องบอกค่าที่ผิดและรูปแบบที่ถูกต้อง
        print_mock.assert_called_once_with(
            "ค่า MQTT_PORT ไม่ถูกต้อง: not-a-number\n"
            "MQTT_PORT ต้องเป็นเลขจำนวนเต็ม"
        )

    # ตรวจว่า Simulator ปฏิเสธ MQTT_HOST ที่เป็นข้อความว่าง
    @patch.dict(
        "simulator.main.os.environ",
        {
            "MQTT_HOST": "   ",
        },
        clear=True,
    )
    @patch("simulator.main.MqttPublisher")
    def test_main_rejects_empty_mqtt_host(
        self,
        mqtt_publisher_class,
    ):
        # เก็บข้อความที่โปรแกรมแสดงไว้ตรวจสอบ
        with patch("builtins.print") as print_mock:
            simulator_main.main()

        # Host ไม่ถูกต้อง จึงต้องยังไม่สร้าง Publisher
        mqtt_publisher_class.assert_not_called()

        # แจ้งให้ผู้ใช้ทราบว่า Host ห้ามเป็นข้อความว่าง
        print_mock.assert_called_once_with(
            "ค่า MQTT_HOST ต้องไม่เป็นข้อความว่าง"
        )

    # ตรวจว่า Simulator ปฏิเสธ Credential ที่กำหนดมาไม่ครบคู่
    @patch.dict(
        "simulator.main.os.environ",
        {
            "MQTT_USERNAME": "simulator",
        },
        clear=True,
    )
    @patch("simulator.main.MqttPublisher")
    def test_main_rejects_incomplete_mqtt_credentials(
        self,
        mqtt_publisher_class,
    ):
        # เก็บข้อความที่โปรแกรมแสดงไว้ตรวจสอบ
        with patch("builtins.print") as print_mock:
            simulator_main.main()

        # Credential ไม่ครบ จึงต้องยังไม่สร้าง Publisher
        mqtt_publisher_class.assert_not_called()

        # ข้อความต้องบอกว่าต้องกำหนด Username และ Password พร้อมกัน
        print_mock.assert_called_once_with(
            "MQTT_USERNAME และ MQTT_PASSWORD "
            "ต้องกำหนดมาคู่กัน"
        )

    # ตรวจว่า Simulator รอแล้วลองส่งใหม่ เมื่อ MQTT ส่งไม่สำเร็จ
    @patch.dict(
        "simulator.main.os.environ",
        {},
        clear=True,
    )
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

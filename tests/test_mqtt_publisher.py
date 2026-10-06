# ใช้ตรวจสอบข้อความ JSON ที่ MqttPublisher เตรียมส่ง
import json

# เครื่องมือทดสอบที่มีมาให้พร้อมกับ Python
import unittest

# สร้างตัวจำลองแทน MQTT Client จริง เพื่อไม่ให้ Test ส่งข้อมูลออกเครือข่าย
from unittest.mock import MagicMock, patch

# นำส่วนที่ส่งข้อมูล MQTT มาเป็นสิ่งที่เราจะทดสอบ
from simulator.mqtt_publisher import MqttPublisher

# นำรูปแบบข้อมูล Telemetry มาใช้สร้างข้อมูลตัวอย่าง
from simulator.telemetry import Telemetry


# รวมการทดสอบของ MqttPublisher ไว้ในกลุ่มเดียวกัน
class TestMqttPublisher(unittest.TestCase):
    # ตรวจว่า Telemetry ถูกส่งไปยัง Topic ที่ถูกต้องในรูปแบบ JSON
    def test_publish_telemetry_sends_correct_topic_and_payload(self):
        # สร้างข้อมูลตัวอย่างที่รู้ค่าทุกช่องล่วงหน้า
        telemetry = Telemetry(
            device_id="ESP32-ROOM-001",
            temperature=30.5,
            humidity=65.0,
            timestamp="2026-09-24T10:00:00+00:00",
        )

        # สร้าง Publisher แต่ยังไม่เชื่อมต่อกับ Broker จริง
        publisher = MqttPublisher(
            host="127.0.0.1",
            port=1883,
        )

        # เปลี่ยน MQTT Client จริงให้เป็นตัวจำลอง
        # เราจึงตรวจสิ่งที่โค้ดสั่งส่งได้โดยไม่ต้องใช้ Mosquitto
        publisher.client = MagicMock()

        # กำหนดให้ข้อความจำลองรายงานว่าส่งสำเร็จ
        publisher.client.publish.return_value.is_published.return_value = True

        # สั่งให้โค้ดเตรียมและส่ง Telemetry
        publisher.publish_telemetry(telemetry)

        # สร้าง JSON ที่เราคาดว่าโค้ดควรส่ง
        expected_payload = json.dumps(
            {
                "device_id": "ESP32-ROOM-001",
                "temperature": 30.5,
                "humidity": 65.0,
                "timestamp": "2026-09-24T10:00:00+00:00",
            },
            ensure_ascii=False,
        )

        # ตรวจว่า publish() ถูกเรียกหนึ่งครั้ง พร้อม Topic, JSON และ QoS ที่ถูกต้อง
        publisher.client.publish.assert_called_once_with(
            topic="pyiot/devices/ESP32-ROOM-001/telemetry",
            payload=expected_payload,
            qos=1,
        )

        # ตรวจว่ารอผลการส่งไม่เกิน 5 วินาที
        publisher.client.publish.return_value.wait_for_publish.assert_called_once_with(
            timeout=5
        )

        # ตรวจว่ามีการถามสถานะว่าข้อความถูกส่งสำเร็จแล้วหรือไม่
        publisher.client.publish.return_value.is_published.assert_called_once_with()

    # ตรวจว่าเกิด TimeoutError เมื่อข้อความยังส่งไม่สำเร็จ
    def test_publish_telemetry_raises_timeout_when_not_published(self):
        # สร้าง Telemetry ตัวอย่างสำหรับใช้ส่ง
        telemetry = Telemetry(
            device_id="ESP32-ROOM-001",
            temperature=30.5,
            humidity=65.0,
            timestamp="2026-09-24T10:00:00+00:00",
        )

        # สร้าง Publisher โดยไม่เชื่อมต่อ Broker จริง
        publisher = MqttPublisher(
            host="127.0.0.1",
            port=1883,
        )
        publisher.client = MagicMock()

        # จำลองว่าหลังจากรอแล้ว ข้อความยังส่งไม่สำเร็จ
        message_info = publisher.client.publish.return_value
        message_info.is_published.return_value = False

        # ตรวจว่าคำสั่งสร้าง TimeoutError พร้อมข้อความที่เข้าใจได้
        with self.assertRaisesRegex(
            TimeoutError,
            "ไม่สามารถส่งข้อมูล MQTT ได้ภายใน 5 วินาที",
        ):
            publisher.publish_telemetry(telemetry)

        # แม้ส่งไม่สำเร็จ โค้ดต้องกำหนดเวลารอไว้ไม่เกิน 5 วินาที
        message_info.wait_for_publish.assert_called_once_with(
            timeout=5
        )

    # ตรวจว่า Publisher เชื่อมต่อไปยัง Broker ตามค่าที่กำหนด
    def test_connect_uses_broker_address_and_starts_loop(self):
        # สร้าง Publisher ด้วยที่อยู่และพอร์ตที่เรารู้ล่วงหน้า
        publisher = MqttPublisher(
            host="127.0.0.1",
            port=1883,
        )

        # ใช้ MQTT Client จำลอง เพื่อไม่เชื่อมต่อเครือข่ายจริง
        publisher.client = MagicMock()

        # เรียกคำสั่งที่ต้องการทดสอบ
        publisher.connect()

        # ตรวจว่า connect() ได้รับที่อยู่ พอร์ต และเวลารักษาการเชื่อมต่อถูกต้อง
        publisher.client.connect.assert_called_once_with(
            host="127.0.0.1",
            port=1883,
            keepalive=60,
        )

        # ตรวจว่าเริ่มระบบดูแลการรับส่งข้อมูลเบื้องหลัง
        publisher.client.loop_start.assert_called_once_with()

    # ตรวจว่า Publisher ยกเลิกการเชื่อมต่อและหยุดงานเบื้องหลัง
    def test_disconnect_stops_client_and_network_loop(self):
        # สร้าง Publisher สำหรับการทดสอบ
        publisher = MqttPublisher(
            host="127.0.0.1",
            port=1883,
        )

        # ใช้ MQTT Client จำลอง จึงไม่กระทบการเชื่อมต่อจริง
        publisher.client = MagicMock()

        # เรียกคำสั่งที่ต้องการทดสอบ
        publisher.disconnect()

        # ตรวจว่ามีการแจ้ง MQTT Client ให้เลิกเชื่อมต่อ
        publisher.client.disconnect.assert_called_once_with()

        # ตรวจว่าระบบทำงานเบื้องหลังถูกหยุด
        publisher.client.loop_stop.assert_called_once_with()

    # ตรวจว่า Username และ Password ถูกส่งให้ Paho Client
    @patch("simulator.mqtt_publisher.mqtt.Client")
    def test_publisher_sets_username_and_password(
        self,
        mqtt_client_class,
    ):
        # สร้าง Paho Client จำลอง
        mqtt_client = MagicMock()
        mqtt_client_class.return_value = mqtt_client

        # สร้าง Publisher พร้อมข้อมูลยืนยันตัวตนตัวอย่าง
        MqttPublisher(
            host="127.0.0.1",
            port=1883,
            username="simulator",
            password="test-password",
        )

        # ตรวจว่า Paho ได้รับ Username และ Password ครบ
        mqtt_client.username_pw_set.assert_called_once_with(
            username="simulator",
            password="test-password",
        )

    # ตรวจว่าไม่ตั้งข้อมูลยืนยันตัวตน เมื่อไม่ได้กำหนด Username
    @patch("simulator.mqtt_publisher.mqtt.Client")
    def test_publisher_skips_authentication_without_username(
        self,
        mqtt_client_class,
    ):
        # สร้าง Paho Client จำลอง
        mqtt_client = MagicMock()
        mqtt_client_class.return_value = mqtt_client

        # สร้าง Publisher โดยไม่ส่ง Username และ Password
        MqttPublisher(
            host="127.0.0.1",
            port=1883,
        )

        # ต้องไม่เรียกคำสั่งตั้ง Username และ Password
        mqtt_client.username_pw_set.assert_not_called()
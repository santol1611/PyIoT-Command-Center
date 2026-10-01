# ใช้เปลี่ยนข้อมูล Python ให้เป็นข้อความ JSON
import json
# ใช้เปลี่ยน Telemetry ซึ่งเป็น dataclass ให้เป็น dictionary
from dataclasses import asdict
# นำเครื่องมือ MQTT Client จาก Paho มาใช้เชื่อมต่อกับ Broker
import paho.mqtt.client as mqtt


# ดูแลการเชื่อมต่อและส่งข้อมูลจาก Simulator ไปยัง MQTT Broker
class MqttPublisher:
    def __init__(
        self,
        host: str,
        port: int,
        client_id: str = "pyiot-simulator",
    ):
        # เก็บที่อยู่และพอร์ตของ Broker ไว้ใช้ตอนเชื่อมต่อ
        self.host = host
        self.port = port

        # สร้าง MQTT Client หนึ่งตัวสำหรับ Simulator
        self.client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=client_id,
            protocol=mqtt.MQTTv311,
        )

    # เชื่อมต่อ Broker และเริ่มดูแลการรับส่งข้อมูล MQTT เบื้องหลัง
    def connect(self):
        self.client.connect(
            host=self.host,
            port=self.port,
            keepalive=60,
        )
        self.client.loop_start()

    # เปลี่ยน Telemetry เป็น JSON แล้วส่งไปยัง Topic ของ Device เครื่องนั้น
    def publish_telemetry(self, telemetry):
        # แต่ละ Device ใช้ Topic ของตัวเอง โดยนำ device_id มาประกอบชื่อ
        topic = f"pyiot/devices/{telemetry.device_id}/telemetry"

        # แปลง Telemetry เป็น dictionary ก่อนเปลี่ยนเป็นข้อความ JSON
        payload = json.dumps(
            asdict(telemetry),
            ensure_ascii=False,
        )

        # QoS 1 ให้ Broker ตอบกลับเพื่อยืนยันว่าได้รับข้อความแล้ว
        message_info = self.client.publish(
            topic=topic,
            payload=payload,
            qos=1,
        )

        # รอจนการส่งข้อความนี้เสร็จ ก่อนทำงานต่อ
        message_info.wait_for_publish()

    # แจ้ง Broker ว่าจะเลิกเชื่อมต่อ แล้วหยุดงานเบื้องหลัง
    def disconnect(self):
        self.client.disconnect()
        self.client.loop_stop()

import json
import time
from dataclasses import asdict

from device import VirtualDevice
from mqtt_publisher import MqttPublisher

def main():
    # สร้างรายการเปล่าสำหรับเก็บ Device
    devices = []
    # สร้าง Device หมายเลข 001 ถึง 010
    for number in range(1, 11):
        device_id = f"ESP32-ROOM-{number:03d}"
        devices.append(
            VirtualDevice(device_id=device_id)
        )

    # สร้างตัวส่งข้อมูล MQTT หนึ่งตัวสำหรับอุปกรณ์จำลองทั้ง 10 เครื่อง
    publisher = MqttPublisher(
        host="127.0.0.1",
        port=1883,
    )

    # เชื่อมต่อกับ Mosquitto ก่อนเริ่มอ่านและส่งข้อมูล
    publisher.connect()

    try:
        # ทำงานซ้ำไปเรื่อย ๆ จนกว่าผู้ใช้จะกด Ctrl+C
        while True:
            for device in devices:
                # อ่านค่า Sensor จาก Device เครื่องนี้
                telemetry = device.collect_telemetry()

                # ส่งข้อมูลไปยัง Mosquitto ผ่าน MQTT
                publisher.publish_telemetry(telemetry)

                # เตรียมข้อมูลสำหรับแสดงในหน้าต่าง CMD
                payload = asdict(telemetry)

                print(
                    json.dumps(
                        payload,
                        indent=4,
                        ensure_ascii=False,
                    )
                )

            # เมื่อครบ 10 เครื่องแล้ว ให้รอ 2 วินาที
            time.sleep(2)

    # ทำงานส่วนนี้เมื่อผู้ใช้กด Ctrl+C
    except KeyboardInterrupt:
        print("\nหยุดการทำงานของ Simulator")

    # ไม่ว่าจะหยุดตามปกติหรือเกิดข้อผิดพลาด ต้องปิด MQTT เสมอ
    finally:
        publisher.disconnect()


# เริ่มทำงานที่ main() เฉพาะเมื่อเปิดไฟล์นี้โดยตรง
if __name__ == "__main__":
    main()

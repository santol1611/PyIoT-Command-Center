import json
import os
import time
from dataclasses import asdict

from device import VirtualDevice
from mqtt_publisher import MqttPublisher

def main():
    # อ่านที่อยู่ Broker จาก Environment Variable
    # หากไม่ได้กำหนดไว้ จะใช้ 127.0.0.1 เป็นค่าเริ่มต้น
    mqtt_host = os.getenv(
        "MQTT_HOST",
        "127.0.0.1",
    ).strip()

    # Environment Variable จะถูกอ่านเป็นข้อความ จึงต้องแปลงพอร์ตเป็นตัวเลข
    mqtt_port_text = os.getenv(
        "MQTT_PORT",
        "1883",
    )

    # MQTT_HOST ต้องไม่เป็นข้อความว่าง
    if not mqtt_host:
        print("ค่า MQTT_HOST ต้องไม่เป็นข้อความว่าง")
        return

    # MQTT_PORT ต้องเป็นเลขจำนวนเต็ม
    try:
        mqtt_port = int(mqtt_port_text)
    except ValueError:
        print(
            f"ค่า MQTT_PORT ไม่ถูกต้อง: {mqtt_port_text}\n"
            "MQTT_PORT ต้องเป็นเลขจำนวนเต็ม"
        )
        return

    # หมายเลข Port ที่ใช้งานได้ต้องอยู่ระหว่าง 1 ถึง 65535
    if not 1 <= mqtt_port <= 65535:
        print(
            f"ค่า MQTT_PORT ไม่ถูกต้อง: {mqtt_port}\n"
            "MQTT_PORT ต้องอยู่ระหว่าง 1 ถึง 65535"
        )
        return

    # อ่านข้อมูลยืนยันตัวตน โดยใช้ค่าว่างเมื่อยังไม่ได้กำหนด
    mqtt_username = os.getenv(
        "MQTT_USERNAME",
        "",
    ).strip()
    mqtt_password = os.getenv(
        "MQTT_PASSWORD",
        "",
    )

    # Username และ Password ต้องกำหนดมาพร้อมกัน
    # ห้ามมีเพียงค่าใดค่าหนึ่ง เพราะจะเชื่อมต่อ Broker ไม่สำเร็จ
    if bool(mqtt_username) != bool(mqtt_password):
        print(
            "MQTT_USERNAME และ MQTT_PASSWORD "
            "ต้องกำหนดมาคู่กัน"
        )
        return

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
        host=mqtt_host,
        port=mqtt_port,
        username=mqtt_username or None,
        password=mqtt_password or None,
    )

    # พยายามเชื่อมต่อกับ Mosquitto ก่อนเริ่มอ่านและส่งข้อมูล
    try:
        publisher.connect()

    # หาก Broker ไม่ทำงานหรือเชื่อมต่อไม่ได้ ให้แสดงข้อความที่อ่านง่าย
    except OSError as error:
        print(
            "ไม่สามารถเชื่อมต่อ MQTT Broker ได้\n"
            f"ที่อยู่: {publisher.host}:{publisher.port}\n"
            f"รายละเอียด: {error}"
        )
        return

    try:
        # ทำงานซ้ำไปเรื่อย ๆ จนกว่าผู้ใช้จะกด Ctrl+C
        while True:
            for device in devices:
                # อ่านค่า Sensor จาก Device เครื่องนี้
                telemetry = device.collect_telemetry()

                # พยายามส่งข้อมูลไปยัง Mosquitto ผ่าน MQTT
                try:
                    publisher.publish_telemetry(telemetry)

                # รับกรณีขาดการเชื่อมต่อหรือรอการส่งเกิน 5 วินาที
                except (RuntimeError, TimeoutError) as error:
                    print(
                        "\nส่งข้อมูล MQTT ไม่สำเร็จ "
                        "กำลังรอ 2 วินาทีก่อนลองใหม่\n"
                        f"รายละเอียด: {error}"
                    )

                    # หยุดรอบของ Device ชั่วคราว เพื่อไม่ให้ผิดพลาดซ้ำ 10 ครั้ง
                    break

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

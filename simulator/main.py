import json
import time
from dataclasses import asdict

from device import VirtualDevice


def main():
    # สร้างอุปกรณ์จำลอง 3 ตัวและเก็บไว้ในรายการเดียวกัน
    devices = [
        VirtualDevice(device_id="ESP32-ROOM-001"),
        VirtualDevice(device_id="ESP32-ROOM-002"),
        VirtualDevice(device_id="ESP32-ROOM-003"),
        VirtualDevice(device_id="ESP32-ROOM-004"),
        VirtualDevice(device_id="ESP32-ROOM-005"),
        VirtualDevice(device_id="ESP32-ROOM-006"),
        VirtualDevice(device_id="ESP32-ROOM-007"),
        VirtualDevice(device_id="ESP32-ROOM-008"),
        VirtualDevice(device_id="ESP32-ROOM-009"),
        VirtualDevice(device_id="ESP32-ROOM-010"),
    ]

    # อ่านและแสดงข้อมูลจากอุปกรณ์ทุกตัวซ้ำไปเรื่อย ๆ
    while True:
        for device in devices:
            telemetry = device.collect_telemetry()
            payload = asdict(telemetry)

            print(
                json.dumps(
                    payload,
                    indent=4,
                    ensure_ascii=False,
                )
            )

        # รอหลังจากอุปกรณ์ทั้ง 3 ตัวส่งข้อมูลครบแล้ว
        time.sleep(2)


# เริ่มทำงานที่ main() เฉพาะเมื่อเปิดไฟล์นี้โดยตรง
if __name__ == "__main__":
    main()

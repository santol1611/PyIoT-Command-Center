import json
import time
from dataclasses import asdict

from device import VirtualDevice


def main():
    # สร้างรายการเปล่าสำหรับเก็บ Device
    devices = []
    # สร้าง Device หมายเลข 001 ถึง 010
    for number in range(1, 11):
        device_id = f"ESP32-ROOM-{number:03d}"
        devices.append(
            VirtualDevice(device_id=device_id)
        )

    while True:
        # อ่านและแสดงข้อมูลจาก Device ทีละเครื่อง
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

        # เมื่อครบ 10 เครื่องแล้ว ให้รอ 2 วินาที
        time.sleep(2)


# เริ่มทำงานที่ main() เฉพาะเมื่อเปิดไฟล์นี้โดยตรง
if __name__ == "__main__":
    main()

import json
import time
from dataclasses import asdict

from device import VirtualDevice


def main():
    # สร้างอุปกรณ์จำลองหนึ่งตัวและกำหนดรหัสประจำอุปกรณ์
    device = VirtualDevice(
        device_id="ESP32-ROOM-001"
    )

    # ทำงานซ้ำไปเรื่อย ๆ เพื่อเลียนแบบอุปกรณ์ที่ส่งค่าตลอดเวลา
    while True:
        # ขอข้อมูลอุณหภูมิและความชื้นชุดล่าสุดจากอุปกรณ์
        telemetry = device.collect_telemetry()

        # เปลี่ยนข้อมูลให้อยู่ในรูปแบบที่นำไปสร้าง JSON ได้
        payload = asdict(telemetry)

        # แสดงข้อมูลให้อ่านง่าย โดยจัดแต่ละรายการแยกเป็นบรรทัด
        print(
            json.dumps(
                payload,
                indent=4,
                ensure_ascii=False,
            )
        )

        # รอ 2 วินาทีก่อนอ่านและแสดงข้อมูลชุดถัดไป
        time.sleep(2)


# เริ่มทำงานที่ main() เฉพาะเมื่อเปิดไฟล์นี้โดยตรง
if __name__ == "__main__":
    main()

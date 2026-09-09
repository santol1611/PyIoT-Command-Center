from sensors.humidity import HumiditySensor
from sensors.temperature import TemperatureSensor
from telemetry import Telemetry


class VirtualDevice:
    # สร้างอุปกรณ์จำลองหนึ่งตัว โดยกำหนดรหัสเพื่อบอกว่าเป็นอุปกรณ์เครื่องใด
    def __init__(self, device_id: str):
        self.device_id = device_id

        # อุปกรณ์หนึ่งตัวมีตัววัดอุณหภูมิและตัววัดความชื้นอยู่ภายใน
        self.temperature_sensor = TemperatureSensor()
        self.humidity_sensor = HumiditySensor()

    def collect_telemetry(self) -> Telemetry:
        # อ่านค่าล่าสุดจากตัววัดทั้งสองชนิด
        temperature = self.temperature_sensor.read()
        humidity = self.humidity_sensor.read()

        # รวมรหัสอุปกรณ์ ค่าที่อ่านได้ และเวลาปัจจุบันไว้เป็นข้อมูลหนึ่งชุด
        return Telemetry.create(
            device_id=self.device_id,
            temperature=temperature,
            humidity=humidity,
        )

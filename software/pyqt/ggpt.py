import asyncio
import bleak
from PyQt5.QtCore import QObject, pyqtSignal, QCoreApplication


class Sensor:
    def __init__(self, device_address, data_characteristic_uuid):
        self.device_address = device_address
        self.data_characteristic_uuid = data_characteristic_uuid
        self.client = None
        self.latest_data = bytearray()

    async def connect(self):
        self.client = bleak.BleakClient(self.device_address)
        await self.client.connect()

    async def disconnect(self):
        if self.client:
            await self.client.disconnect()
            self.client = None

    async def read_sensor_data(self):
        if self.client:
            data = await self.client.read_gatt_char(self.data_characteristic_uuid)
            self.latest_data = bytearray(data)

    def get_latest_data(self):
        return self.latest_data

async def initialize_sensor(device_address, data_characteristic_uuid):
    sensor = Sensor(device_address, data_characteristic_uuid)
    await sensor.connect()
    return sensor

async def get_sensor_data(sensor):
    await sensor.read_sensor_data()
    return sensor.get_latest_data()

async def close_sensor(sensor):
    await sensor.disconnect()

if __name__ == "__main__":
    device_address = 'F2:E3:5C:1A:6D:96'
    data_characteristic_uuid = '21370005-2137-2137-2137-213721372137'
    AFS_SEL = 1
    ACC_SCALE_FACTOR = (2 ** AFS_SEL) / 16384.0

    loop = asyncio.get_event_loop()
    sensor = loop.run_until_complete(initialize_sensor(device_address, data_characteristic_uuid))
    while True:
        buf = loop.run_until_complete(get_sensor_data(sensor))
        # print("Latest Sensor Data:", data.hex())

        acc_x = ACC_SCALE_FACTOR * int.from_bytes(buf[0:2], byteorder="little", signed=True)
        acc_y = ACC_SCALE_FACTOR * int.from_bytes(buf[2:4], byteorder="little", signed=True)
        acc_z = ACC_SCALE_FACTOR * int.from_bytes(buf[4:6], byteorder="little", signed=True)

        print(acc_x, acc_y, acc_z)
    loop.run_until_complete(close_sensor(sensor))
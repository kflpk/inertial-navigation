from bleak import BleakScanner
from bleak import BleakClient
import asyncio
import threading

class Sensor:
    def __init__(self):
        self.uuid_sensor_service    = "21370001-2137-2137-2137-213721372137"
        self.uuid_sensor_char       = "21370005-2137-2137-2137-213721372137"
        self.address = "F2:E3:5C:1A:6D:96"
        self.AFS_SEL = 1
        self.ACC_SCALE_FACTOR = (2 ** self.AFS_SEL) / 16384.0

        self.FS_SEL = 1
        self.GYRO_SCALE_FACTOR = (2 ** self.FS_SEL) / 131.0

        self.MAG_SCALE_FACTOR = 2.56

        self.acc_x = []
        self.acc_y = []
        self.acc_z = []
        self.gyr_x = []
        self.gyr_y = []
        self.gyr_z = []
        self.mag_x = []
        self.mag_y = []
        self.mag_z = []
        self.asyncio_time = []

    async def get_sensor_data(self):
        async with BleakClient(self.address) as client:
            await client.get_services()
            buf = await client.read_gatt_char(self.uuid_sensor_char)
            acc_x = self.ACC_SCALE_FACTOR * int.from_bytes(buf[0:2], byteorder="little", signed=True)
            acc_y = self.ACC_SCALE_FACTOR * int.from_bytes(buf[2:4], byteorder="little", signed=True)
            acc_z = self.ACC_SCALE_FACTOR * int.from_bytes(buf[4:6], byteorder="little", signed=True)

            self.acc_x.append(acc_x)
            self.acc_y.append(acc_y)
            self.acc_z.append(acc_z)
            self.asyncio_time.append(asyncio.get_event_loop().time())
        
            return acc_x, acc_y, acc_z

#class BLEWorker(QObject):
    #data_received = pyqtSignal(str)

    #async def receive_data(self):
        #while True:
            ## Your data receiving logic here
            ## Example: Read a characteristic value from a connected BLE device
            #data = await self.client.read_gatt_char('00002a00-0000-1000-8000-00805f9b34fb')
            
            ## Emit a signal with the received data
            #self.data_received.emit(data.decode())

    #def start_ble_communication(self):
        #async def _start_ble_communication():
            #self.client = bleak.BleakClient('device_address')
            #await self.client.connect()
            #await self.receive_data()

        #asyncio.run(_start_ble_communication())
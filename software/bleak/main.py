import asyncio
from bleak import BleakScanner, BleakClient
import time

uuid_sensor_service = "21370001-2137-2137-2137-213721372137"
uuid_acc_char       = "21370005-2137-2137-2137-213721372137"
uuid_gyro_char      = "21370003-2137-2137-2137-213721372137"
uuid_mag_char       = "21370004-2137-2137-2137-213721372137"
address = "F2:E3:5C:1A:6D:96"
AFS_SEL = 1
ACC_SCALE_FACTOR = (2 ** AFS_SEL) / 16384.0

FS_SEL = 1
GYRO_SCALE_FACTOR = (2 ** FS_SEL) / 131.0

MAG_SCALE_FACTOR = 2.56

async def main():
    devices = await BleakScanner.discover()
    print(devices)

    while True:
        async with BleakClient(address) as client:
            while True:
                svcs = await client.get_services()
                buf  = await client.read_gatt_char(uuid_acc_char)
                acc_x  = ACC_SCALE_FACTOR  * int.from_bytes(buf[0:2],   byteorder='big', signed=True)
                acc_y  = ACC_SCALE_FACTOR  * int.from_bytes(buf[2:4],   byteorder='big', signed=True)
                acc_z  = ACC_SCALE_FACTOR  * int.from_bytes(buf[4:6],   byteorder='big', signed=True)
                gyro_x = GYRO_SCALE_FACTOR * int.from_bytes(buf[6:8],   byteorder='big', signed=True)
                gyro_y = GYRO_SCALE_FACTOR * int.from_bytes(buf[8:10],  byteorder='big', signed=True)
                gyro_z = GYRO_SCALE_FACTOR * int.from_bytes(buf[10:12], byteorder='big', signed=True)
                mag_x  = MAG_SCALE_FACTOR  * int.from_bytes(buf[12:14], byteorder='big', signed=True)
                mag_y  = MAG_SCALE_FACTOR  * int.from_bytes(buf[14:16], byteorder='big', signed=True)
                mag_z  = MAG_SCALE_FACTOR  * int.from_bytes(buf[16:18], byteorder='big', signed=True)
                print("acc:  ", acc_x, acc_y, acc_z)
                print("gyro: ", gyro_x, gyro_y, gyro_z)
                print("mag:  ", mag_x, mag_y, mag_z)

        # async with BleakClient(address) as client:
        #     my_service, = (s for s in client.get_services() if s.uuid == uuid_sensor_service)
        #     my_char = my_service.get_characteristic(uuid_acc_char)
        #     client.read_gatt_char(my_char)

asyncio.run(main())
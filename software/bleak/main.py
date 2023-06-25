import asyncio
from bleak import BleakScanner, BleakClient
import time

uuid_sensor_service = "21370001-2137-2137-2137-213721372137"
uuid_sensor_char       = "21370005-2137-2137-2137-213721372137"
address = "F2:E3:5C:1A:6D:96"
AFS_SEL = 1
ACC_SCALE_FACTOR = (2 ** AFS_SEL) / 16384.0

FS_SEL = 1
GYRO_SCALE_FACTOR = (2 ** FS_SEL) / 131.0

MAG_SCALE_FACTOR = 2.56

async def main():
    devices = await BleakScanner.discover()
    print(devices)
    width = 7
    precision = 2

    while True:
        async with BleakClient(address) as client:
            while True:
                svcs = await client.get_services()
                buf  = await client.read_gatt_char(uuid_sensor_char)
                acc_x  = ACC_SCALE_FACTOR  * int.from_bytes(buf[0:2],   byteorder='little', signed=True)
                acc_y  = ACC_SCALE_FACTOR  * int.from_bytes(buf[2:4],   byteorder='little', signed=True)
                acc_z  = ACC_SCALE_FACTOR  * int.from_bytes(buf[4:6],   byteorder='little', signed=True)
                gyro_x = GYRO_SCALE_FACTOR * int.from_bytes(buf[6:8],   byteorder='little', signed=True)
                gyro_y = GYRO_SCALE_FACTOR * int.from_bytes(buf[8:10],  byteorder='little', signed=True)
                gyro_z = GYRO_SCALE_FACTOR * int.from_bytes(buf[10:12], byteorder='little', signed=True)
                mag_x  = MAG_SCALE_FACTOR  * int.from_bytes(buf[12:14], byteorder='little', signed=True)
                mag_y  = MAG_SCALE_FACTOR  * int.from_bytes(buf[14:16], byteorder='little', signed=True)
                mag_z  = MAG_SCALE_FACTOR  * int.from_bytes(buf[16:18], byteorder='little', signed=True)
                print(f"acc:  {acc_x:{width}.{precision}f}; {acc_y:{width}.{precision}f}; {acc_z:{width}.{precision}f}")
                print(f"gyro: {gyro_x:{width}.{precision}f}; {gyro_y:{width}.{precision}f}; {gyro_z:{width}.{precision}f}")
                print(f"mag:  {mag_x:{width}.{precision}f}; {mag_y:{width}.{precision}f}; {mag_z:{width}.{precision}f}")

asyncio.run(main())
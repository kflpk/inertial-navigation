import asyncio
import time
import pandas as pd
from bleak import BleakScanner, BleakClient
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument("--num_samples", "-n", type=int, help="Num samples to collect.")
parser.add_argument("--save_to_file", "-s", type=str, default=None, help="Save results to a file.")
parser.add_argument(
    "--load_from_file",
    "-l",
    type=str,
    default=None,
    help="Load results from a file and skip collecting samples.",
)
args = parser.parse_args()

uuid_sensor_service = "21370001-2137-2137-2137-213721372137"
uuid_sensor_char = "21370005-2137-2137-2137-213721372137"
address = "F2:E3:5C:1A:6D:96"
AFS_SEL = 1
ACC_SCALE_FACTOR = (2**AFS_SEL) / 16384.0

FS_SEL = 1
GYRO_SCALE_FACTOR = (2**FS_SEL) / 131.0

MAG_SCALE_FACTOR = 2.56


class SensorData:
    def __init__(self):
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


async def get_sensor_data():
    sensor_data = SensorData()
    async with BleakClient(address) as client:
        while True:
            await client.get_services()
            buf = await client.read_gatt_char(uuid_sensor_char)
            acc_x = ACC_SCALE_FACTOR * int.from_bytes(buf[0:2], byteorder="little", signed=True)
            acc_y = ACC_SCALE_FACTOR * int.from_bytes(buf[2:4], byteorder="little", signed=True)
            acc_z = ACC_SCALE_FACTOR * int.from_bytes(buf[4:6], byteorder="little", signed=True)
            gyr_x = GYRO_SCALE_FACTOR * int.from_bytes(buf[6:8], byteorder="little", signed=True)
            gyr_y = GYRO_SCALE_FACTOR * int.from_bytes(buf[8:10], byteorder="little", signed=True)
            gyr_z = GYRO_SCALE_FACTOR * int.from_bytes(buf[10:12], byteorder="little", signed=True)
            mag_x = MAG_SCALE_FACTOR * int.from_bytes(buf[12:14], byteorder="little", signed=True)
            mag_y = MAG_SCALE_FACTOR * int.from_bytes(buf[14:16], byteorder="little", signed=True)
            mag_z = MAG_SCALE_FACTOR * int.from_bytes(buf[16:18], byteorder="little", signed=True)

            sensor_data.acc_x.append(acc_x)
            sensor_data.acc_y.append(acc_y)
            sensor_data.acc_z.append(acc_z)
            sensor_data.gyr_x.append(gyr_x)
            sensor_data.gyr_y.append(gyr_y)
            sensor_data.gyr_z.append(gyr_z)
            sensor_data.mag_x.append(mag_x)
            sensor_data.mag_y.append(mag_y)
            sensor_data.mag_z.append(mag_z)
            sensor_data.asyncio_time.append(asyncio.get_event_loop().time())

            if len(sensor_data.acc_x) > args.num_samples:
                return sensor_data


def main():
    if args.save_to_file and args.load_from_file:
        raise ValueError("Cannot save to file and load from file at the same time.")

    if args.load_from_file and args.num_samples:
        raise ValueError("Cannot load from file and collect samples at the same time.")

    if args.load_from_file:
        csv = pd.read_csv(args.load_from_file)

        sensor_data = SensorData()
        sensor_data.acc_x = csv["acc_x"].tolist()
        sensor_data.acc_y = csv["acc_y"].tolist()
        sensor_data.acc_z = csv["acc_z"].tolist()
        sensor_data.gyr_x = csv["gyr_x"].tolist()
        sensor_data.gyr_y = csv["gyr_y"].tolist()
        sensor_data.gyr_z = csv["gyr_z"].tolist()
        sensor_data.mag_x = csv["mag_x"].tolist()
        sensor_data.mag_y = csv["mag_y"].tolist()
        sensor_data.mag_z = csv["mag_z"].tolist()
        sensor_data.asyncio_time = csv["asyncio_time"].tolist()

    elif args.num_samples:
        print("dupa")
        sensor_data = asyncio.run(get_sensor_data())

        if args.save_to_file:
            df = pd.DataFrame(
                {
                    "acc_x": sensor_data.acc_x,
                    "acc_y": sensor_data.acc_y,
                    "acc_z": sensor_data.acc_z,
                    "gyr_x": sensor_data.gyr_x,
                    "gyr_y": sensor_data.gyr_y,
                    "gyr_z": sensor_data.gyr_z,
                    "mag_x": sensor_data.mag_x,
                    "mag_y": sensor_data.mag_y,
                    "mag_z": sensor_data.mag_z,
                    "asyncio_time": sensor_data.asyncio_time,
                }
            )
            df.to_csv(args.save_to_file)

    # i w tym miejscu mamy obiekt klasy SensorData, ktory mozemy przetwarzac jak chcemy
main()
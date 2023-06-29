from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QCoreApplication, QEventLoop, QThread, pyqtSignal
import asyncio
import bleak


class BLEWorker(QThread):
    data_received = pyqtSignal(bytes)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.read_sensor_data())

    async def read_sensor_data(self):
        async with bleak.BleakScanner() as scanner:
            devices = await scanner.discover()
            device = devices[0]  # Assuming the sensor device is the first discovered device
            async with bleak.BleakClient("F2:E3:5C:1A:6D:96") as client:
                while True:
                    # Read the sensor data characteristic
                    sensor_data_char = await client.read_gatt_char('21370005-2137-2137-2137-213721372137')
                    self.data_received.emit(sensor_data_char)


class SensorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sensor Application")

        layout = QVBoxLayout()
        label = QLabel("Sensor Data:")
        layout.addWidget(label)

        self.sensor_data_label = QLabel()
        layout.addWidget(self.sensor_data_label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.worker = BLEWorker()
        self.worker.data_received.connect(self.update_sensor_data)

    def update_sensor_data(self, data):
        sensor_data_hex = data.hex()
        self.sensor_data_label.setText(sensor_data_hex)

    def start_ble_communication(self):
        self.worker.start()

    def run(self):
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    window = SensorApp()
    window.run()
    app.exec_()

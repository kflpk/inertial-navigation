from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread
import asyncio
import bleak
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QTextEdit, QWidget

class BLEWorker(QObject):
    data_received = pyqtSignal(bytearray)

    async def receive_data(self):
        while True:
            # Your data receiving logic here
            # Example: Read a characteristic value from a connected BLE device
            data = await self.client.read_gatt_char('21370005-2137-2137-2137-213721372137')
            
            # Emit a signal with the received data
            self.data_received.emit(data)

    def start_ble_communication(self):
        async def _start_ble_communication():
            self.client = bleak.BleakClient('F2:E3:5C:1A:6D:96')
            await self.client.connect()
            await self.receive_data()

        asyncio.run(_start_ble_communication())

class BLEApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BLE Application")
        
        # Create a layout
        layout = QVBoxLayout()

        # Add a label
        label = QLabel("Bluetooth Low Energy Application")
        layout.addWidget(label)

        # Add a button to start BLE communication
        button = QPushButton("Start BLE Communication")
        button.clicked.connect(self.start_ble_communication_threaded)
        layout.addWidget(button)

        # Add a text box to display received data
        self.data_textbox = QTextEdit()
        self.data_textbox.setReadOnly(True)
        layout.addWidget(self.data_textbox)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Create a BLE worker
        self.worker = BLEWorker()
        self.worker.data_received.connect(self.update_data)

        # Create a thread for the BLE worker
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.start_ble_communication)
        self.thread.start()

    def update_data(self, data):
        self.hex_data = data.hex()
        self.data_textbox.append(hex_data)

    def start_ble_communication_threaded(self):
        # Start the BLE communication in the worker thread
        self.thread.start()

    def run(self):
        self.show()

    def closeEvent(self, event):
        self.thread.quit()
        self.thread.wait()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication([])
    window = BLEApp()
    window.run()
    app.exec_()

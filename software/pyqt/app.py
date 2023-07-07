from PyQt5 import QtGui
from sensor import *
import sys
from PyQt5.QtCore import (
    QFile,
    QLine,
    qUnregisterResourceData,
    Qt,
    pyqtSignal,
    QThread,
    QObject,
)
from PyQt5.QtWidgets import (
    QAction,
    QGridLayout,
    QHBoxLayout,
    QLayout,
    QMenuBar,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QSpinBox,
    QDoubleSpinBox,
    QApplication,
    QMenu,
    QFileDialog,
    QTableWidget,
    QLabel,
    QCheckBox,
    QMainWindow,
    QTableWidgetItem,
)
import pyqtgraph as pg
import numpy as np
import pandas as pd
from functools import partial
from pyqtgraph import PlotWidget
import bleak

AFS_SEL = 1
ACC_SCALE_FACTOR = (2**AFS_SEL) / 16384.0

device_address = "F2:E3:5C:1A:6D:96"
data_characteristic_uuid = "21370005-2137-2137-2137-213721372137"


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


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.fp = 10.0
        self.dt = 1 / self.fp
        self.sensor = Sensor(device_address, data_characteristic_uuid)

        ########## WINDOW PROPERTIES ############
        self.set_window_properties()

        ############ PLOT AND TABLE ############
        self.plot_widget = PlotWidget()

        self._sidebar_init()

        self.setCentralWidget(QWidget(self))
        self.layout = QHBoxLayout(self.centralWidget())
        self.layout.addLayout(self.sidebar_layout)
        self.layout.addWidget(self.plot_widget)
        self.plot_widget.setYRange(-4, 4)

    def _sidebar_init(self):
        ### SENSOR READINGS
        self.reading_label = QLabel("<b>Sensor readings</b>",  self, alignment=Qt.AlignmentFlag.AlignCenter)

        self.xlabel = QLabel("X acceleration: ", self)
        self.xval = QLabel("0.00", self)
        self.xlayout = QHBoxLayout()
        self.xlayout.addWidget(self.xlabel)
        self.xlayout.addWidget(self.xval)

        self.ylabel = QLabel("Y acceleration: ", self)
        self.yval = QLabel("0.00", self)
        self.ylayout = QHBoxLayout()
        self.ylayout.addWidget(self.ylabel)
        self.ylayout.addWidget(self.yval)

        self.zlabel = QLabel("Z acceleration: ", self)
        self.zval = QLabel("0.00", self)
        self.zlayout = QHBoxLayout()
        self.zlayout.addWidget(self.zlabel)
        self.zlayout.addWidget(self.zval)

        self.reading_layout = QVBoxLayout(self)
        self.reading_layout.addWidget(self.reading_label)
        self.reading_layout.addLayout(self.xlayout)
        self.reading_layout.addLayout(self.ylayout)
        self.reading_layout.addLayout(self.zlayout)
        self.reading_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        ### /SENSOR READINGS

        ### BLUETOOTH
        self.bt_title = QLabel("<b>Bluetooth</b>", self, alignment=Qt.AlignmentFlag.AlignCenter)
        self.bt_connect_button = QPushButton("Connect", self)
        self.bt_connect_button.clicked.connect(self.start_ble_connection)
        self.bt_disconnect_button = QPushButton("Disconnect", self)

        self.bt_buttons_layout = QHBoxLayout(self)
        self.bt_buttons_layout.addWidget(self.bt_connect_button)
        self.bt_buttons_layout.addWidget(self.bt_disconnect_button)
        self.bt_disconnect_button.clicked.connect(self.stop_ble_connection)
        self.bluetooth_state_label = QLabel("Bluetooth: disconnected", self)

        self.bluetooth_layout = QVBoxLayout(self)
        self.bluetooth_layout.addWidget(self.bt_title)
        self.bluetooth_layout.addLayout(self.bt_buttons_layout)
        self.bluetooth_layout.addWidget(self.bluetooth_state_label)
        self.bluetooth_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        ### /BLUETOOTH

        self.sidebar_layout = QVBoxLayout(self)
        self.sidebar_layout.addLayout(self.reading_layout)
        self.sidebar_layout.addLayout(self.bluetooth_layout)
        # self.sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def set_window_properties(self):
        self.title = "Akcelerometr"
        self.height = 500
        self.width = 1060

        self.setMinimumHeight(100)
        self.setMinimumWidth(100)
        self.setGeometry(400, 250, self.width, self.height)
        self.setWindowTitle(self.title)

    def init_plots(self):
        penwidth = 2

        self.pen_x = pg.mkPen(color="#D22D72", width=penwidth)
        self.pen_y = pg.mkPen(color="#72D22D", width=penwidth)
        self.pen_z = pg.mkPen(color="#2D72D2", width=penwidth)

        self.plot_x = self.plot_widget.plot(pen=self.pen_x, name="X axis")
        self.plot_y = self.plot_widget.plot(pen=self.pen_y, name="Y axis")
        self.plot_z = self.plot_widget.plot(pen=self.pen_z, name="Z axis")

        self.time_data = np.arange(0, 5, self.dt)
        self.data_x = 0 * self.time_data
        self.data_y = 0 * self.time_data
        self.data_z = 0 * self.time_data

        self.plot_x.setData(self.time_data, self.data_x)
        self.plot_y.setData(self.time_data, self.data_y)
        self.plot_z.setData(self.time_data, self.data_z)

    def start_timer(self):
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(1000 * self.dt)

    def stop_timer(self):
        self.timer.stop()

    def update_plots(self):
        txtformat = "{data:8.2f} g"
        time_last = self.time_data[-1]
        self.time_data[:-1] = self.time_data[1:]
        self.time_data[-1] = time_last + self.dt

        try:
            buf = self.loop.run_until_complete(get_sensor_data(self.sensor))
            acc_x = ACC_SCALE_FACTOR * int.from_bytes(
                buf[0:2], byteorder="little", signed=True
            )
            acc_y = ACC_SCALE_FACTOR * int.from_bytes(
                buf[2:4], byteorder="little", signed=True
            )
            acc_z = ACC_SCALE_FACTOR * int.from_bytes(
                buf[4:6], byteorder="little", signed=True
            )

            self.data_x[:-1] = self.data_x[1:]
            self.data_x[-1] = acc_x
            self.xval.setText(txtformat.format(data=self.data_x[-1]))

            self.data_y[:-1] = self.data_y[1:]
            self.data_y[-1] = acc_y
            self.yval.setText(txtformat.format(data=self.data_y[-1]))

            self.data_z[:-1] = self.data_z[1:]
            self.data_z[-1] = acc_z
            self.zval.setText(txtformat.format(data=self.data_z[-1]))

            self.plot_x.setData(self.time_data, self.data_x)
            self.plot_y.setData(self.time_data, self.data_y)
            self.plot_z.setData(self.time_data, self.data_z)
        except bleak.exc.BleakError:
            print("Device disconnected")
            self.stop_ble_connection()

    def start_ble_connection(self):
        try:
            self.sensor = self.loop.run_until_complete(
                initialize_sensor(device_address, data_characteristic_uuid)
            )
            self.bluetooth_state_label.setText("Bluetooth connected")
            self.start_timer()
        except:
            print("Error: coudln't connect to the sensor")

    def stop_ble_connection(self):
        try:
            if self.sensor:
                self.loop.run_until_complete(close_sensor(self.sensor))
            self.sensor = None
            self.bluetooth_state_label.setText("Bluetooth disconnected")
            self.stop_timer()
        except:
            print("Device already disonnected")

    def run(self):
        self.set_window_properties()
        self.init_plots()
        self.loop = asyncio.get_event_loop()

        self.show()

    def closeEvent(self, event) -> None:
        self.stop_ble_connection()

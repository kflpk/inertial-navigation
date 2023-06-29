from sensor import *
import sys
from PyQt5.QtCore import QFile, QLine, qUnregisterResourceData, Qt, pyqtSignal, QThread, QObject
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

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.fp = 30.0
        self.dt = 1/self.fp
        self.marg = Sensor()

        ########## WINDOW PROPERTIES ############
        self.set_window_properties()

        ############ PLOT AND TABLE ############
        self.plot_widget = PlotWidget()

        self._sidebar_init()

        self.setCentralWidget(QWidget(self))
        self.layout = QHBoxLayout(self.centralWidget())
        self.layout.addLayout(self.sidebar_layout)
        self.layout.addWidget(self.plot_widget)

        ########## BLE ###########
        self.worker = BLEWorker()
        self.worker.data_received.connect(self.update_plots)

        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.start_ble_communication)
    
    def start_ble_connection(self):
        self.thread.start()

    def stop_ble_connection(self):
        exit()

    def _sidebar_init(self):
        ### SENSOR READINGS 
        self.reading_label = QLabel(self)
        self.reading_label.setText("<b>Sensor readings</b>")
        self.reading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.xlabel = QLabel(self)
        self.xlabel.setText("X Acceleration: ")
        self.xval = QLabel(self)
        self.xlayout = QHBoxLayout()
        self.xlayout.addWidget(self.xlabel)
        self.xlayout.addWidget(self.xval)

        self.ylabel = QLabel(self)
        self.ylabel.setText("Y Acceleration: ")
        self.yval = QLabel(self)
        self.ylayout = QHBoxLayout()
        self.ylayout.addWidget(self.ylabel)
        self.ylayout.addWidget(self.yval)

        self.zlabel = QLabel(self)
        self.zval = QLabel(self)
        self.zlabel.setText("Z Acceleration: ")
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
        self.bt_title = QLabel(self)
        self.bt_title.setText("<b>Bluetooth</b>")
        self.bt_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bt_connect_button = QPushButton(self)
        self.bt_connect_button.setText("Connect")
        self.bt_connect_button.clicked.connect(self.start_ble_connection)
        self.bt_disconnect_button = QPushButton(self)
        self.bt_disconnect_button.setText("Disconnect")

        self.bt_buttons_layout = QHBoxLayout(self)
        self.bt_buttons_layout.addWidget(self.bt_connect_button)
        self.bt_buttons_layout.addWidget(self.bt_disconnect_button)
        self.bt_disconnect_button.clicked.connect(self.stop_ble_connection)
        self.bluetooth_state_label = QLabel(self)
        self.bluetooth_state_label.setText("Bluetooth: disconnected")

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
        penwidth=2

        self.pen_x = pg.mkPen(color="#D22D72", width=penwidth)
        self.pen_y = pg.mkPen(color="#72D22D", width=penwidth)
        self.pen_z = pg.mkPen(color="#2D72D2", width=penwidth)

        self.plot_x = self.plot_widget.plot(pen=self.pen_x, name="X axis")
        self.plot_y = self.plot_widget.plot(pen=self.pen_y, name="Y axis")
        self.plot_z = self.plot_widget.plot(pen=self.pen_z, name="Z axis")

        self.time_data = np.arange(0, 5, self.dt)
        self.data_x = np.sin(1*np.pi * self.time_data - 2*np.pi/3)
        self.data_y = np.sin(1*np.pi * self.time_data - 4*np.pi/3)
        self.data_z = np.sin(1*np.pi * self.time_data - 6*np.pi/3)

        self.plot_x.setData(self.time_data, self.data_x)
        self.plot_y.setData(self.time_data, self.data_y)
        self.plot_z.setData(self.time_data, self.data_z)

    def start_timer(self):
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(1000 * self.dt)

    
    def update_plots(self):
        txtformat = "{data:8.2f}"
        time_last = self.time_data[-1]
        self.time_data[:-1] = self.time_data[1:]
        self.time_data[-1] = time_last + self.dt

        self.data_x[:-1] = self.data_x[1:]
        self.data_x[-1] = np.sin(1*np.pi * time_last - 2*np.pi/3)
        self.xval.setText(txtformat.format(data=self.data_x[-1]))

        self.data_y[:-1] = self.data_y[1:]
        self.data_y[-1] = np.sin(1*np.pi * time_last - 4*np.pi/3)
        self.yval.setText(txtformat.format(data=self.data_y[-1]))

        self.data_z[:-1] = self.data_z[1:]
        self.data_z[-1] = np.sin(1*np.pi * time_last - 6*np.pi/3)
        self.zval.setText(txtformat.format(data=self.data_z[-1]))

        self.plot_x.setData(self.time_data, self.data_x)
        self.plot_y.setData(self.time_data, self.data_y)
        self.plot_z.setData(self.time_data, self.data_z)

    def run(self):
        self.set_window_properties()
        self.init_plots()
        self.start_timer()
        self.show()
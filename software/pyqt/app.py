from PyQt5 import QtGui
from sensor import *
import sys
import time
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
import socket

AFS_SEL = 1
FS_SEL  = 1
ACC_SCALE_FACTOR = (2**AFS_SEL) / 16384.0
MAG_SCALE_FACTOR = 2.56
GYR_SCALE_FACTOR = (2 ** FS_SEL) / 131.0

esp_ip = "192.168.0.201"
esp_port = 3333

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.fp = 15.0
        self.dt = 1 / self.fp
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        ########## WINDOW PROPERTIES ############
        self.set_window_properties()

        ############ PLOT AND TABLE ############
        self.acc_plot_widget = PlotWidget()
        self.gyr_plot_widget = PlotWidget()
        self.mag_plot_widget = PlotWidget()

        self._sidebar_init()

        self.setCentralWidget(QWidget(self))
        self.layout = QHBoxLayout(self.centralWidget())
        self.plots_layout = QGridLayout()
        self.layout.addLayout(self.sidebar_layout)
        self.layout.addLayout(self.plots_layout)
        self.plots_layout.addWidget(self.acc_plot_widget, 0, 0)
        self.plots_layout.addWidget(self.gyr_plot_widget, 0, 1)
        self.plots_layout.addWidget(self.mag_plot_widget, 1, 0)

        self.acc_plot_widget.setYRange(-4, 4)
        self.gyr_plot_widget.setYRange(-500, 500)
        self.mag_plot_widget.setYRange(-4, 4)

    def _sidebar_init(self):
        ### SENSOR READINGS
        self.reading_label = QLabel("<b>Sensor readings</b>",  self, alignment=Qt.AlignmentFlag.AlignCenter)

        self.xlabel = QLabel("X acceleration: ", self)
        self.acc_xval = QLabel("0.00", self)
        self.xlayout = QHBoxLayout()
        self.xlayout.addWidget(self.xlabel)
        self.xlayout.addWidget(self.acc_xval)

        self.ylabel = QLabel("Y acceleration: ", self)
        self.acc_yval = QLabel("0.00", self)
        self.ylayout = QHBoxLayout()
        self.ylayout.addWidget(self.ylabel)
        self.ylayout.addWidget(self.acc_yval)

        self.zlabel = QLabel("Z acceleration: ", self)
        self.acc_zval = QLabel("0.00", self)
        self.zlayout = QHBoxLayout()
        self.zlayout.addWidget(self.zlabel)
        self.zlayout.addWidget(self.acc_zval)

        self.reading_layout = QVBoxLayout(self)
        self.reading_layout.addWidget(self.reading_label)
        self.reading_layout.addLayout(self.xlayout)
        self.reading_layout.addLayout(self.ylayout)
        self.reading_layout.addLayout(self.zlayout)
        self.reading_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        ### /SENSOR READINGS

        ### BLUETOOTH
        self.bt_title = QLabel("<b>TCP</b>", self, alignment=Qt.AlignmentFlag.AlignCenter)
        self.bt_connect_button = QPushButton("Connect", self)
        self.bt_connect_button.clicked.connect(self.start_tcp_connection)
        self.bt_disconnect_button = QPushButton("Disconnect", self)

        self.bt_buttons_layout = QHBoxLayout(self)
        self.bt_buttons_layout.addWidget(self.bt_connect_button)
        self.bt_buttons_layout.addWidget(self.bt_disconnect_button)
        self.bt_disconnect_button.clicked.connect(self.stop_tcp_connection)
        self.tcp_state_label = QLabel("Disconnected", self)

        self.bluetooth_layout = QVBoxLayout(self)
        self.bluetooth_layout.addWidget(self.bt_title)
        self.bluetooth_layout.addLayout(self.bt_buttons_layout)
        self.bluetooth_layout.addWidget(self.tcp_state_label)
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

        self.acc_plot_x = self.acc_plot_widget.plot(pen=self.pen_x, name="X axis")
        self.acc_plot_y = self.acc_plot_widget.plot(pen=self.pen_y, name="Y axis")
        self.acc_plot_z = self.acc_plot_widget.plot(pen=self.pen_z, name="Z axis")

        self.gyr_plot_x = self.gyr_plot_widget.plot(pen=self.pen_x, name="X axis")
        self.gyr_plot_y = self.gyr_plot_widget.plot(pen=self.pen_y, name="Y axis")
        self.gyr_plot_z = self.gyr_plot_widget.plot(pen=self.pen_z, name="Z axis")

        self.mag_plot_x = self.mag_plot_widget.plot(pen=self.pen_x, name="X axis")
        self.mag_plot_y = self.mag_plot_widget.plot(pen=self.pen_y, name="Y axis")
        self.mag_plot_z = self.mag_plot_widget.plot(pen=self.pen_z, name="Z axis")

        self.time_data = np.arange(0, 5, self.dt)

        self.acc_data_x = 0 * self.time_data
        self.acc_data_y = 0 * self.time_data
        self.acc_data_z = 0 * self.time_data

        self.gyr_data_x = 0 * self.time_data
        self.gyr_data_y = 0 * self.time_data
        self.gyr_data_z = 0 * self.time_data

        self.mag_data_x = 0 * self.time_data
        self.mag_data_y = 0 * self.time_data
        self.mag_data_z = 0 * self.time_data


        self.acc_plot_x.setData(self.time_data, self.acc_data_x)
        self.acc_plot_y.setData(self.time_data, self.acc_data_y)
        self.acc_plot_z.setData(self.time_data, self.acc_data_z)

        self.gyr_plot_x.setData(self.time_data, self.gyr_data_x)
        self.gyr_plot_y.setData(self.time_data, self.gyr_data_y)
        self.gyr_plot_z.setData(self.time_data, self.gyr_data_z)

        self.mag_plot_x.setData(self.time_data, self.mag_data_x)
        self.mag_plot_y.setData(self.time_data, self.mag_data_y)
        self.mag_plot_z.setData(self.time_data, self.mag_data_z)

    def start_timer(self):
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(1000 * self.dt)

    def stop_timer(self):
        self.timer.stop()

    def update_plots(self):
        # start = time.time()

        txtformat = "{data:8.2f} g"
        # time_last = self.time_data[-1]
        # self.time_data[:-1] = self.time_data[1:]
        # self.time_data[-1] = time_last + self.dt

        try:
            # buf = self.loop.run_until_complete(get_sensor_data(self.sensor))
            self.sock.sendall(b'r')
            buf = self.sock.recv(20)


            delta_t = 0.001 * int.from_bytes(buf[0:2], byteorder='little', signed=False)
            time_last = self.time_data[-1]
            self.time_data[:-1] = self.time_data[1:]
            self.time_data[-1] = time_last + delta_t



            acc_x = ACC_SCALE_FACTOR * int.from_bytes(
                buf[2:4], byteorder="little", signed=True
            )
            acc_y = ACC_SCALE_FACTOR * int.from_bytes(
                buf[4:6], byteorder="little", signed=True
            )
            acc_z = ACC_SCALE_FACTOR * int.from_bytes(
                buf[6:8], byteorder="little", signed=True
            )

            gyr_x = GYR_SCALE_FACTOR * int.from_bytes(
                buf[8:10], byteorder="little", signed=True
            )
            gyr_y = GYR_SCALE_FACTOR * int.from_bytes(
                buf[10:12], byteorder="little", signed=True
            )
            gyr_z = GYR_SCALE_FACTOR * int.from_bytes(
                buf[12:14], byteorder="little", signed=True
            )

            mag_x = MAG_SCALE_FACTOR * int.from_bytes(
                buf[14:16], byteorder="little", signed=True
            )
            mag_y = MAG_SCALE_FACTOR * int.from_bytes(
                buf[16:18], byteorder="little", signed=True
            )
            mag_z = MAG_SCALE_FACTOR * int.from_bytes(
                buf[18:20], byteorder="little", signed=True
            )

            self.acc_data_x[:-1] = self.acc_data_x[1:]
            self.acc_data_x[-1] = acc_x
            self.acc_xval.setText(txtformat.format(data=self.acc_data_x[-1]))

            self.acc_data_y[:-1] = self.acc_data_y[1:]
            self.acc_data_y[-1] = acc_y
            self.acc_yval.setText(txtformat.format(data=self.acc_data_y[-1]))

            self.acc_data_z[:-1] = self.acc_data_z[1:]
            self.acc_data_z[-1] = acc_z
            self.acc_zval.setText(txtformat.format(data=self.acc_data_z[-1]))

            self.gyr_data_x[:-1] = self.gyr_data_x[1:]
            self.gyr_data_x[-1] = gyr_x
            # self.gyr_xval.setText(txtformat.format(data=self.gyr_data_x[-1]))

            self.gyr_data_y[:-1] = self.gyr_data_y[1:]
            self.gyr_data_y[-1] = gyr_y
            # self.gyr_yval.setText(txtformat.format(data=self.gyr_data_y[-1]))

            self.gyr_data_z[:-1] = self.gyr_data_z[1:]
            self.gyr_data_z[-1] = gyr_z
            # self.gyr_zval.setText(txtformat.format(data=self.gyr_data_z[-1]))

            self.mag_data_x[:-1] = self.mag_data_x[1:]
            self.mag_data_x[-1] = mag_x
            # self.mag_xval.setText(txtformat.format(data=self.mag_data_x[-1]))

            self.mag_data_y[:-1] = self.mag_data_y[1:]
            self.mag_data_y[-1] = mag_y
            # self.mag_yval.setText(txtformat.format(data=self.mag_data_y[-1]))

            self.mag_data_z[:-1] = self.mag_data_z[1:]
            self.mag_data_z[-1] = mag_z
            # self.mag_zval.setText(txtformat.format(data=self.mag_data_z[-1]))

            self.acc_plot_x.setData(self.time_data, self.acc_data_x)
            self.acc_plot_y.setData(self.time_data, self.acc_data_y)
            self.acc_plot_z.setData(self.time_data, self.acc_data_z)

            self.gyr_plot_x.setData(self.time_data, self.gyr_data_x)
            self.gyr_plot_y.setData(self.time_data, self.gyr_data_y)
            # self.gyr_plot_z.setData(self.time_data, self.gyr_data_z)

            self.mag_plot_x.setData(self.time_data, self.mag_data_x)
            self.mag_plot_y.setData(self.time_data, self.mag_data_y)
            self.mag_plot_z.setData(self.time_data, self.mag_data_z)
        except Exception as ex:
            print(ex)
            # self.stop_tcp_connection()
        # stop = time.time()
        # print("execution time: {}".format(stop-start))

    def start_tcp_connection(self):
        try:
            self.sock.connect((esp_ip, esp_port))
            self.tcp_state_label.setText(f"Connected to {esp_ip}:{esp_port}")
            self.start_timer()
        except:
            print("Error: coudln't connect to the sensor")

    def stop_tcp_connection(self):
        try:
            self.sock.close()
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_state_label.setText("Disconnected")
            self.stop_timer()
        except:
            print("Device already disonnected")

    def run(self):
        self.set_window_properties()
        self.init_plots()

        self.show()

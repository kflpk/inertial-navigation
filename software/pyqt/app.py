from PyQt5 import QtGui
from sensor import *
import sys
import math as m
import time
from ahrs.filters import Madgwick
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
FS_SEL = 1
ACC_SCALE_FACTOR =  9.81 * (2**AFS_SEL) / 16384.0
MAG_SCALE_FACTOR = 0.024414062
GYR_SCALE_FACTOR = (2*np.pi / 360) * (2**FS_SEL) / 131.0

esp_ip = "192.168.0.201"
esp_port = 3333

def euler_from_quaternion(x, y, z, w):  # getting roll pitch yaw from quaternions
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = m.atan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = m.asin(t2)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = m.atan2(t3, t4)

    return roll_x, pitch_y, yaw_z  # in radians


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.fp = 10
        self.dt = 1 / self.fp
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.madgwick = Madgwick()
        self.Q = np.tile((1., 0., 0., 0.), 1)      # Allocation of quaternions
        print(self.Q.shape)
        # self.gx, self.gy, self.gz = [], [], []
        self.gx_off = -0.03528160630975249
        self.gy_off = 0.060357828314595866
        self.gz_off = -0.0195740506736186


        ########## WINDOW PROPERTIES ############
        self.set_window_properties()

        ############ PLOT AND TABLE ############
        self.acc_plot_widget = PlotWidget()
        self.gyr_plot_widget = PlotWidget()
        self.mag_plot_widget = PlotWidget()
        self.euler_plot_widget = PlotWidget()

        self._sidebar_init()

        self.setCentralWidget(QWidget(self))
        self.layout = QHBoxLayout(self.centralWidget())
        self.plots_layout = QGridLayout()
        self.layout.addLayout(self.sidebar_layout)
        self.layout.addLayout(self.plots_layout)
        self.plots_layout.addWidget(self.acc_plot_widget, 0, 0)
        self.plots_layout.addWidget(self.gyr_plot_widget, 0, 1)
        self.plots_layout.addWidget(self.mag_plot_widget, 1, 0)
        self.plots_layout.addWidget(self.euler_plot_widget, 1, 1)

        self.acc_plot_widget.setYRange(-4*9.81, 4*9.81)
        self.gyr_plot_widget.setYRange(-6.28, 6.28)
        self.mag_plot_widget.setYRange(-800, 800)
        self.euler_plot_widget.setYRange(-np.pi, np.pi)

    def _sidebar_init(self):
        ### SENSOR READINGS
        self.reading_label = QLabel(
            "<b>Sensor readings</b>", self, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.acc_xval = QLabel("0.00", self)
        self.acc_yval = QLabel("0.00", self)
        self.acc_zval = QLabel("0.00", self)

        self.gyr_xval = QLabel("0.00", self)
        self.gyr_yval = QLabel("0.00", self)
        self.gyr_zval = QLabel("0.00", self)

        self.mag_xval = QLabel("0.00", self)
        self.mag_yval = QLabel("0.00", self)
        self.mag_zval = QLabel("0.00", self)

        self.yaw_val = QLabel("0.00", self)
        self.pitch_val = QLabel("0.00", self)
        self.roll_val = QLabel("0.00", self)

        self.reading_layout = QVBoxLayout(self)
        self.reading_layout.addWidget(self.reading_label)
        # self.reading_layout.addLayout(self.xlayout)
        # self.reading_layout.addLayout(self.ylayout)
        # self.reading_layout.addLayout(self.zlayout)
        self.sensor_layout = QGridLayout(self)

        self.sensor_layout.addWidget(QLabel("X acceleration: ", self), 0, 0)
        self.sensor_layout.addWidget(self.acc_xval, 0, 1)
        self.sensor_layout.addWidget(QLabel("Y acceleration: ", self), 1, 0)
        self.sensor_layout.addWidget(self.acc_yval, 1, 1)
        self.sensor_layout.addWidget(QLabel("Z acceleration: ", self), 2, 0)
        self.sensor_layout.addWidget(self.acc_zval, 2, 1)

        self.sensor_layout.addWidget(QLabel("X rotation: ", self), 3, 0)
        self.sensor_layout.addWidget(self.gyr_xval, 3, 1)
        self.sensor_layout.addWidget(QLabel("Y rotation: ", self), 4, 0)
        self.sensor_layout.addWidget(self.gyr_yval, 4, 1)
        self.sensor_layout.addWidget(QLabel("Z rotation: ", self), 5, 0)
        self.sensor_layout.addWidget(self.gyr_zval, 5, 1)

        self.sensor_layout.addWidget(QLabel("X mag: ", self), 6, 0)
        self.sensor_layout.addWidget(self.mag_xval, 6, 1)
        self.sensor_layout.addWidget(QLabel("Y mag: ", self), 7, 0)
        self.sensor_layout.addWidget(self.mag_yval, 7, 1)
        self.sensor_layout.addWidget(QLabel("Z mag: ", self), 8, 0)
        self.sensor_layout.addWidget(self.mag_zval, 8, 1)

        self.sensor_layout.addWidget(QLabel("Yaw: ", self), 9, 0)
        self.sensor_layout.addWidget(self.yaw_val, 9, 1)
        self.sensor_layout.addWidget(QLabel("Pitch: ", self), 10, 0)
        self.sensor_layout.addWidget(self.pitch_val, 10, 1)
        self.sensor_layout.addWidget(QLabel("Roll: ", self), 11, 0)
        self.sensor_layout.addWidget(self.roll_val, 11, 1)

        self.sensor_layout.addWidget(self.acc_zval)

        self.reading_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.reading_layout.addLayout(self.sensor_layout)
        ### /SENSOR READINGS

        ### BLUETOOTH
        self.bt_title = QLabel(
            "<b>TCP</b>", self, alignment=Qt.AlignmentFlag.AlignCenter
        )
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

        self.yaw_plot   = self.euler_plot_widget.plot(pen=self.pen_x, name="Yaw")
        self.pitch_plot = self.euler_plot_widget.plot(pen=self.pen_y, name="Pitch")
        self.roll_plot  = self.euler_plot_widget.plot(pen=self.pen_z, name="Roll")

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

        self.yaw_data   = 0 * self.time_data
        self.pitch_data = 0 * self.time_data
        self.roll_data  = 0 * self.time_data

        self.acc_plot_x.setData(self.time_data, self.acc_data_x)
        self.acc_plot_y.setData(self.time_data, self.acc_data_y)
        self.acc_plot_z.setData(self.time_data, self.acc_data_z)

        self.gyr_plot_x.setData(self.time_data, self.gyr_data_x)
        self.gyr_plot_y.setData(self.time_data, self.gyr_data_y)
        self.gyr_plot_z.setData(self.time_data, self.gyr_data_z)

        self.mag_plot_x.setData(self.time_data, self.mag_data_x)
        self.mag_plot_y.setData(self.time_data, self.mag_data_y)
        self.mag_plot_z.setData(self.time_data, self.mag_data_z)

        self.yaw_plot.setData(self.time_data, self.yaw_data)
        self.pitch_plot.setData(self.time_data, self.pitch_data)
        self.roll_plot.setData(self.time_data, self.roll_data)


    def start_timer(self):
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(int(1000 * self.dt))

    def stop_timer(self):
        self.timer.stop()

    def update_plots(self):
        # start = time.time()

        txtformat = "{data:8.2f} {unit}"
        # time_last = self.time_data[-1]
        # self.time_data[:-1] = self.time_data[1:]
        # self.time_data[-1] = time_last + self.dt

        try:
            # buf = self.loop.run_until_complete(get_sensor_data(self.sensor))
            self.sock.sendall(b"r")
            buf = self.sock.recv(20)

            delta_t = 0.001 * int.from_bytes(buf[0:2], byteorder="little", signed=False)

            # #### UPDATE MADGWICK FILTER
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
            # self.gx.append(gyr_x)
            # self.gy.append(gyr_y)
            # self.gz.append(gyr_z)
            gyr_x -= self.gx_off
            gyr_y -= self.gy_off
            gyr_z -= self.gz_off

            self.madgwick.Dt = delta_t
            self.Q = self.madgwick.updateMARG(
                self.Q,
                gyr=[gyr_x, gyr_y, gyr_z],
                acc=[acc_x, acc_y, acc_z],
                mag=[mag_x, mag_y, mag_z],
            )
            roll, pitch, yaw = euler_from_quaternion(self.Q[1], self.Q[2], self.Q[3], self.Q[0])
            # print(roll, pitch, yaw)

            self.acc_data_x[:-1] = self.acc_data_x[1:]
            self.acc_data_x[-1] = acc_x
            self.acc_xval.setText(txtformat.format(data=acc_x, unit="m/s^2"))

            self.acc_data_y[:-1] = self.acc_data_y[1:]
            self.acc_data_y[-1] = acc_y
            self.acc_yval.setText(txtformat.format(data=acc_y, unit="m/s^2"))

            self.acc_data_z[:-1] = self.acc_data_z[1:]
            self.acc_data_z[-1] = acc_z
            self.acc_zval.setText(txtformat.format(data=acc_z, unit="m/s^2"))

            self.gyr_data_x[:-1] = self.gyr_data_x[1:]
            self.gyr_data_x[-1] = gyr_x
            self.gyr_xval.setText(txtformat.format(data=gyr_x, unit="rad/s"))

            self.gyr_data_y[:-1] = self.gyr_data_y[1:]
            self.gyr_data_y[-1] = gyr_y
            self.gyr_yval.setText(txtformat.format(data=gyr_y, unit="rad/s"))

            self.gyr_data_z[:-1] = self.gyr_data_z[1:]
            self.gyr_data_z[-1] = gyr_z
            self.gyr_zval.setText(txtformat.format(data=gyr_z, unit="rad/s"))

            self.mag_data_x[:-1] = self.mag_data_x[1:]
            self.mag_data_x[-1] = mag_x
            self.mag_xval.setText(txtformat.format(data=mag_x, unit="µT"))

            self.mag_data_y[:-1] = self.mag_data_y[1:]
            self.mag_data_y[-1] = mag_y
            self.mag_yval.setText(txtformat.format(data=mag_y, unit="µT"))

            self.mag_data_z[:-1] = self.mag_data_z[1:]
            self.mag_data_z[-1] = mag_z
            self.mag_zval.setText(txtformat.format(data=mag_z, unit="µT"))

            self.yaw_data[:-1] = self.yaw_data[1:]
            self.yaw_data[-1] = yaw
            self.yaw_val.setText(txtformat.format(data=yaw, unit="rad"))

            self.pitch_data[:-1] = self.pitch_data[1:]
            self.pitch_data[-1] = pitch
            self.pitch_val.setText(txtformat.format(data=pitch, unit="rad"))

            self.roll_data[:-1] = self.roll_data[1:]
            self.roll_data[-1] = roll
            self.roll_val.setText(txtformat.format(data=roll, unit="rad"))

            self.acc_plot_x.setData(self.time_data, self.acc_data_x)
            self.acc_plot_y.setData(self.time_data, self.acc_data_y)
            self.acc_plot_z.setData(self.time_data, self.acc_data_z)

            self.gyr_plot_x.setData(self.time_data, self.gyr_data_x)
            self.gyr_plot_y.setData(self.time_data, self.gyr_data_y)
            self.gyr_plot_z.setData(self.time_data, self.gyr_data_z)

            self.mag_plot_x.setData(self.time_data, self.mag_data_x)
            self.mag_plot_y.setData(self.time_data, self.mag_data_y)
            self.mag_plot_z.setData(self.time_data, self.mag_data_z)

            self.yaw_plot.setData(self.time_data, self.yaw_data)
            self.pitch_plot.setData(self.time_data, self.pitch_data)
            self.roll_plot.setData(self.time_data, self.roll_data)

        except Exception as ex:
            print(ex)
            # self.stop_tcp_connection()
        # stop = time.time()
        # print("execution time: {}".format(stop-start))

    def start_tcp_connection(self):
        # try:
        self.sock.connect((esp_ip, esp_port))
        self.tcp_state_label.setText(f"Connected to {esp_ip}:{esp_port}")
        self.start_timer()
        # except:
        #     print("Error: couldn't connect to the sensor")

    def stop_tcp_connection(self):
        # try:
        self.sock.close()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_state_label.setText("Disconnected")
        self.stop_timer()

    def run(self):
        self.set_window_properties()
        self.init_plots()

        self.show()

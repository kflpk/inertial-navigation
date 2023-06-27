
import sys
from PyQt5.QtCore import QFile, QLine, qUnregisterResourceData
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

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.fp = 30.0
        self.dt = 1/self.fp

        ########## WINDOW PROPERTIES ############
        self.set_window_properties()

        ############ PLOT AND TABLE ############
        self.graph = pg.PlotWidget()
        self.fft_graph = pg.PlotWidget()
        self.plot_widget = PlotWidget()
        self.setCentralWidget(self.plot_widget)


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

        self.plot_x = self.plot_widget.plot(pen=self.pen_x)
        self.plot_y = self.plot_widget.plot(pen=self.pen_y)
        self.plot_z = self.plot_widget.plot(pen=self.pen_z)

        self.time_data = np.arange(0, 5, self.dt)
        self.data_x = np.sin(1*np.pi * self.time_data - 2*np.pi/3)
        self.data_y = np.sin(1*np.pi * self.time_data - 4*np.pi/3)
        self.data_z = np.sin(1*np.pi * self.time_data - 6*np.pi/3)

        self.plot_x.setData(self.time_data, self.data_x)
        self.plot_y.setData(self.time_data, self.data_y)
        self.plot_z.setData(self.time_data, self.data_z)

    def declare_actions(self):
        pass

    def start_timer(self):
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(1000 * self.dt)

    
    def update_plots(self):
        time_last = self.time_data[-1]
        self.time_data[:-1] = self.time_data[1:]
        self.time_data[-1] = time_last + self.dt

        self.data_x[:-1] = self.data_x[1:]
        self.data_x[-1] = np.sin(1*np.pi * time_last - 2*np.pi/3)

        self.data_y[:-1] = self.data_y[1:]
        self.data_y[-1] = np.sin(1*np.pi * time_last - 4*np.pi/3)

        self.data_z[:-1] = self.data_z[1:]
        self.data_z[-1] = np.sin(1*np.pi * time_last - 6*np.pi/3)

        self.plot_x.setData(self.time_data, self.data_x)
        self.plot_y.setData(self.time_data, self.data_y)
        self.plot_z.setData(self.time_data, self.data_z)

    def run(self):
        self.set_window_properties()
        self.init_plots()
        self.start_timer()
        self.show()
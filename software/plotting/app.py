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
import pyqtgraph.opengl as gl
import fft
import numpy as np
import pandas as pd
from functools import partial
from scipy.io.wavfile import write

from generator import Function_generator


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.waveform = "Sine"  # temporary

        ########## WINDOW PROPERTIES ############
        self.title = "Function generator"
        self.setWindowTitle(self.title)

        self.setMinimumHeight(500)
        self.height = 100
        self.width = int(1060)
        self.setGeometry(400, 250, self.width, self.height)

        ############# ACTIONS  ##################

        ############ LAYOUTS ####################
        self.window_container = QHBoxLayout()
        self.plot_container = QVBoxLayout()
        self.container = QVBoxLayout()
        self.upper = QVBoxLayout()
        self.lower = QGridLayout()
        self.left = QVBoxLayout()
        self.right = QVBoxLayout()

        self.x_layout = QVBoxLayout()
        self.y_layout = QVBoxLayout()
        self.z_layout = QVBoxLayout()

        self.window_container.addLayout(self.container)
        self.window_container.addLayout(self.plot_container)

        self.container.addLayout(self.upper)
        self.container.addLayout(self.lower)

        self.upper.addLayout(self.left)
        self.upper.addLayout(self.right)

        self.left.addLayout(self.x_layout)
        self.left.addLayout(self.y_layout)
        self.left.addLayout(self.z_layout)

        ########### WIDGETS ##################
        self.x_box = QDoubleSpinBox()
        self.x_label = QLabel(self)
        self.x_label.setText("Acceleration X")

        self.y_box = QDoubleSpinBox()
        self.y_label = QLabel(self)
        self.y_label.setText("Acceleration Y")

        self.z_box = QDoubleSpinBox()
        self.z_label = QLabel(self)
        self.z_label.setText("Acceleration Z")

        self.generate_button = QPushButton("Generate", self)

        self.x_box.setRange(0, 5)
        self.x_box.setValue(1)
        self.x_box.setSingleStep(0.05)

        self.x_layout.addWidget(self.x_label)
        self.x_layout.addWidget(self.x_box)

        self.y_layout.addWidget(self.y_label)
        self.y_layout.addWidget(self.y_box)

        self.z_layout.addWidget(self.z_label)
        self.z_layout.addWidget(self.z_box)

        ############ PLOT AND TABLE ############
        self.graph = pg.PlotWidget()
        # self.fft_graph = pg.PlotWidget()
        # self.table = QTableWidget(self)

        self.plot_container.addWidget(self.graph)
        # self.plot_container.addWidget(self.fft_graph)
        # self.table_container.addWidget(self.table)


        self.pen = pg.mkPen(color="#DB1252", width=3)
        # self.fft_pen = pg.mkPen(color="#DB1252", width=1)
        self.graph.setRange(xRange=[0, 0.015])
        # self.fft_graph.setRange(xRange=[0, 20000])

        self.setLayout(self.window_container)
        

        # self.show()
        self.view = gl.GLViewWidget()
        self.xgrid = gl.GLGridItem()
        self.ygrid = gl.GLGridItem()
        self.zgrid = gl.GLGridItem()
        self.view.addItem(self.xgrid)
        self.view.addItem(self.ygrid)
        self.view.addItem(self.zgrid)
        self.view.setBackgroundColor('w')
        self.view.opts['viewport'] =  (0, 0, 1920, 1080)
        self.view.show()

    def update_data(self):

        data_points_number = len(self.time_vector)

        # FUNCTION PLOT
        self.graph.clear()
        self.main_plot = self.graph.plot(
            self.time_vector,
            self.waveform_data,
            pen=self.pen,
        )

        # FOURIERS PLOT
        self.fft_graph.clear()
        if self.fft_button.checkState() == 2:
            self.fft_plot = self.fft_graph.plot(
                self.fft_freq,
                self.fft_val,
                pen=self.pen
            )
        print("fft done plottin")


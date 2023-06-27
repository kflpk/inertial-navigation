
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

class App(QWidget):
    def __init__(self):
        super().__init__()
        ########## WINDOW PROPERTIES ############
        self.set_window_properties()

        ############ PLOT AND TABLE ############
        self.graph = pg.PlotWidget()
        self.fft_graph = pg.PlotWidget()

        self.show()

    def set_window_properties(self):
        self.title = "Akcelerometr"
        self.height = 100
        self.width = int(1060)

        self.setMinimumHeight(500)
        self.setGeometry(400, 250, self.width, self.height)
        self.setWindowTitle(self.title)
    
    def init_plots(self):
        penwidth=3
        self.pen_x = pg.mkPen(color="#f41e0e", width=penwidth)
        self.pen_x = pg.mkPen(color="#f4910e", width=penwidth)
        self.pen_x = pg.mkPen(color="#0ea8f4", width=penwidth)

    def declare_actions(self):
        pass
    
    def update_plots(self):
        pass
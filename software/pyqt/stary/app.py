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
        self.save = QAction("Save", self)
        self.save.triggered.connect(self.save_file)

        self.load = QAction("Load", self)
        self.load.triggered.connect(self.load_file)

        ############# MENU BAR ##################
        # self.menu = QMenuBar(self)
        # self.file_menu = self.menu.addMenu("File")
        # self.help_menu = self.menu.addMenu("Help")

        # self.file_menu.addActions([self.save, self.load])
        # self.help_menu.addAction(self.about)

        ############ LAYOUTS ####################
        self.window_container = QHBoxLayout()
        self.plot_container = QVBoxLayout()
        self.table_container = QHBoxLayout()
        self.container = QVBoxLayout()
        self.upper = QVBoxLayout()
        self.lower = QGridLayout()
        self.left = QVBoxLayout()
        self.right = QVBoxLayout()

        self.sampling_layout = QVBoxLayout()
        self.frequency_layout = QVBoxLayout()
        self.time_layout = QVBoxLayout()
        self.amp_layout = QVBoxLayout()

        self.window_container.addLayout(self.container)
        self.window_container.addLayout(self.plot_container)
        self.window_container.addLayout(self.table_container)

        self.container.addLayout(self.upper)
        self.container.addLayout(self.lower)

        self.upper.addLayout(self.left)
        self.upper.addLayout(self.right)

        self.left.addLayout(self.sampling_layout)
        self.left.addLayout(self.frequency_layout)
        self.left.addLayout(self.time_layout)
        self.left.addLayout(self.amp_layout)

        ########### WIDGETS ##################

        self.sampling_box = QSpinBox()
        self.freq_box = QDoubleSpinBox()
        self.time_box = QSpinBox()
        self.amp_box = QDoubleSpinBox()

        self.sampling_label = QLabel(self)
        self.freq_label = QLabel(self)
        self.time_label = QLabel(self)
        self.amp_label = QLabel(self)
        self.source_label = QLabel(self)

        self.sampling_label.setText("Sampling rate")
        self.freq_label.setText("Frequency")
        self.amp_label.setText("Amplitude")
        self.time_label.setText("Time")

        self.generate_button = QPushButton("Generate", self)
        self.load_button = QPushButton("Load file", self)
        self.save_csv_button = QPushButton("Save as csv", self)
        self.save_wav_button = QPushButton("Save as wav", self)
        self.save_fft_button = QPushButton("Save FFT", self)

        self.sampling_box.setRange(1000, 100000)
        self.sampling_box.setSingleStep(10000)
        self.sampling_box.setValue(44100)

        self.freq_box.setRange(0, 25000)
        self.freq_box.setValue(440)
        self.freq_box.setSingleStep(10)

        self.time_box.setRange(0, 3600)
        self.time_box.setValue(15)
        self.time_box.setSingleStep(1)

        self.amp_box.setRange(0, 5)
        self.amp_box.setValue(1)
        self.amp_box.setSingleStep(0.05)

        self.waveform_label = QLabel(self)
        self.waveform_label.setText("Waveform")
        self.sine_button = QRadioButton("Sine", self)
        self.saw_button = QRadioButton("Sawtooth", self)
        self.square_button = QRadioButton("Square", self)
        self.white_button = QRadioButton("White Noise", self)
        self.fft_button = QCheckBox("FFT", self)
        self.table_button = QCheckBox("Table", self)
        self.fft_button.setChecked(True)

        self.spin_boxes = [self.sampling_box, self.freq_box, self.time_box]
        self.radio_buttons = [
            self.sine_button,
            self.saw_button,
            self.square_button,
            self.white_button,
        ]

        self.sampling_layout.addWidget(self.sampling_label)
        self.sampling_layout.addWidget(self.sampling_box)

        self.frequency_layout.addWidget(self.freq_label)
        self.frequency_layout.addWidget(self.freq_box)

        self.time_layout.addWidget(self.time_label)
        self.time_layout.addWidget(self.time_box)

        self.amp_layout.addWidget(self.amp_label)
        self.amp_layout.addWidget(self.amp_box)

        self.right.addWidget(self.waveform_label)

        self.generate_button.clicked.connect(self.generate_data)

        for button in self.radio_buttons:
            self.right.addWidget(button)

        self.right.addWidget(self.fft_button)
        self.right.addWidget(self.table_button)

        self.lower.addWidget(self.generate_button, 0, 0, 1, 1)
        self.lower.addWidget(self.load_button, 0, 1, 1, 1)
        self.lower.addWidget(self.save_csv_button, 1, 0, 1, 1)
        self.lower.addWidget(self.save_wav_button, 2, 0, 1, 1)
        self.lower.addWidget(self.save_fft_button, 1, 1, 1, 1)

        self.load_button.clicked.connect(self.load_file)

        ############ RADIO BUTTONS  ############

        self.sine_button.clicked.connect(partial(self.set_waveform, "Sine"))
        self.saw_button.clicked.connect(partial(self.set_waveform, "Sawtooth"))
        self.square_button.clicked.connect(partial(self.set_waveform, "Square"))
        self.white_button.clicked.connect(partial(self.set_waveform, "White Noise"))

        ########### STUFFFF ####################
        
        self.save_csv_button.clicked.connect(self.save_data_csv)
        self.save_wav_button.clicked.connect(self.save_data_wav)
        self.save_fft_button.clicked.connect(self.save_fft_csv)

        ############ PLOT AND TABLE ############
        self.graph = pg.PlotWidget()
        self.fft_graph = pg.PlotWidget()
        self.table = QTableWidget(self)

        self.plot_container.addWidget(self.graph)
        self.plot_container.addWidget(self.fft_graph)
        self.table_container.addWidget(self.table)

        self.table.setRowCount(15)
        self.table.setColumnCount(2)
        self.table.setMinimumWidth(250)

        self.pen = pg.mkPen(color="#DB1252", width=3)
        self.fft_pen = pg.mkPen(color="#DB1252", width=1)
        self.graph.setRange(xRange=[0, 0.015])
        self.fft_graph.setRange(xRange=[0, 20000])

        self.sine_button.toggle()
        self.setLayout(self.window_container)
        self.show()

    def load_file(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "", options=options
        )

        df = pd.read_csv(filename, sep="\t")
        self.time_vector = np.array(df["t"])
        self.waveform_data = np.array(df["v"])

        self.update_data()

    def save_file(self):
        pass

    def save_data_csv(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "QFileDialog.getOpenFileName()",
            f"{self.waveform}.csv",
            options=options,
        )
        # file = open(filename, "w")
        # file.write("Hemlo Worlmd")
        # file.close()

        csv_data = {"t": self.time_vector, "v": self.waveform_data}
        dataframe = pd.DataFrame(csv_data)
        dataframe.to_csv(filename, index=False, sep="\t")

    def save_data_wav(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "QFileDialog.getOpenFileName()",
            f"{self.waveform}.wav",
            options=options,
        )
        audio_data = np.int16(self.waveform_data * 2 ** 14)
        write(filename, self.sampling_box.value(), audio_data)

    def save_fft_csv(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "QFileDialog.getOpenFileName()",
            f"{self.waveform}_fft.csv",
            options=options,
        )
        csv_data = {"f": self.fft_freq, "a": self.fft_val}
        dataframe = pd.DataFrame(csv_data)
        dataframe.to_csv(filename, index=False, sep="\t")

    def generate_data(self):
        generator = Function_generator(self.sampling_box.value(), self.time_box.value())

        functions = {
            "Sine": generator.sine,
            "Sawtooth": generator.sawtooth,
            "Square": generator.square,
            "White Noise": generator.WhiteNoise,
        }

        self.time_vector = generator.time_vector()
        self.waveform_data = functions[self.waveform](
            self.amp_box.value(), self.freq_box.value()
        )

        self.fft_freq, self.fft_val = fft.fouriers_transform(
            self.time_vector, self.waveform_data
        )
        self.update_data()

    def load_data(self):
        self.update_data()

    def update_data(self):

        data_points_number = len(self.time_vector)

        # VALUE TABLE
        if self.table_button.checkState() == 2:
            self.table.setRowCount(data_points_number)
            for i in range(0, data_points_number):
                self.table.setItem(
                    i, 0, QTableWidgetItem(str(float("%.4g" % self.time_vector[i])))
                )
                self.table.setItem(
                    i, 1, QTableWidgetItem(str(float("%.4g" % self.waveform_data[i])))
                )
                print(i, self.time_vector[i], self.waveform_data[i])

        # FUNCTION PLOT
        self.graph.clear()
        # print("graphing new plot")
        self.main_plot = self.graph.plot(
            self.time_vector,
            self.waveform_data,
            pen=self.pen,
        )

        # FOURIERS PLOT
        self.fft_graph.clear()
        if self.fft_button.checkState() == 2:
            # print("graphing new fft")
            self.fft_plot = self.fft_graph.plot(
                self.fft_freq,
                self.fft_val,
                pen=self.pen
            )
        print("fft done plottin")

    def set_waveform(self, waveform: str) -> None:
        self.waveform = waveform
        if waveform == "White Noise":
            self.fft_button.setChecked(0)
        print(self.waveform)

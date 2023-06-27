import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow
from pyqtgraph import PlotWidget, mkPen

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Multiple Sine Waves")
        self.resize(800, 600)

        self.plot_widget = PlotWidget()
        self.setCentralWidget(self.plot_widget)

    def init_plots(self):
        self.plots = []
        self.plot_data = []

        num_plots = 4
        colors = ["r", "g", "b", "c"]
        self.phases = [0, np.pi/4, np.pi/2, 3*np.pi/4]
        self.t = 0

        for i in range(num_plots):
            plot = self.plot_widget.plot()
            data = np.sin(np.linspace(0, 10, 100) + self.phases[i])
            self.plots.append(plot)
            self.plot_data.append(data)

            pen = mkPen(color=colors[i])
            plot.setPen(pen)

            x_data = np.linspace(0, 10, 100)
            plot.setData(x_data, data)

    def update_plots(self):
        self.t += 1
        for plot, data, phase in zip(self.plots, self.plot_data, self.phases):
            data[:-1] = data[1:]
            data[-1] = np.sin(self.t/10 - phase)

            x_data = np.linspace(0, 10, 100)
            plot.setData(x_data, data)

    def start_timer(self):
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(70)

    def run(self):
        self.init_plots()
        self.start_timer()
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.run()
    sys.exit(app.exec_())

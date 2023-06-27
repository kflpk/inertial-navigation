import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from pyqtgraph import PlotWidget
class MainWindow(QMainWindow):
    def __init__(self):
        self.counter = 1
        super(MainWindow, self).__init__()
        self.setWindowTitle("Multiple Plots on One Graph")
        self.resize(800, 600)

        # Create the plot widget
        self.plot_widget = PlotWidget()
        self.setCentralWidget(self.plot_widget)
    def init_plots(self):
        # Create multiple plots
        self.plots = []
        self.plot_data = []
        # Initialize plot data
        num_plots = 4  # Number of plots to create
        for i in range(num_plots):
            plot = self.plot_widget.plot()
            data = np.random.rand(100)
            self.plots.append(plot)
            self.plot_data.append(data)

            # Set the x and y data for the initial plot
            x_data = np.linspace(0, 10, 100)
            plot.setData(x_data, data)
    def update_plots(self):
        self.counter += 1
        # Update data for each plot
        for plot, data in zip(self.plots, self.plot_data):
            data[:-1] = data[1:]
            data[-1] = np.random.rand()

            # Update the plot with new data
            x_data = np.linspace(0, 10, 100)
            plot.setData(x_data, data)
    def start_timer(self):
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(100)  # Update plots every 100 milliseconds (10 Hz)
    def run(self):
        self.init_plots()
        self.start_timer()
        self.show()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.run()
    sys.exit(app.exec_())

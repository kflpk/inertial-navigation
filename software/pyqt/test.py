import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from pyqtgraph import PlotWidget
from PyQt5.QtCore import QTimer
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Live Updating Plot")
        self.resize(800, 600)

        # Create the plot widget
        self.plot_widget = PlotWidget()
        self.setCentralWidget(self.plot_widget)
    def init_plot(self):
        # Create an empty plot
        self.plot = self.plot_widget.plot()

        # Initialize x and y data
        self.x_data = np.linspace(0, 10, 100)
        self.y_data = np.random.rand(100)

        # Set the x and y data for the initial plot
        self.plot.setData(self.x_data, self.y_data)
    def init_plot(self):
        # Create an empty plot
        self.plot = self.plot_widget.plot()

        # Initialize x and y data
        self.x_data = np.linspace(0, 10, 100)
        self.y_data = np.random.rand(100)

        # Set the x and y data for the initial plot
        self.plot.setData(self.x_data, self.y_data)

    def start_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)  # Update plot every 100 milliseconds (10 Hz)
    def update_plot(self):
        # Generate new y data
        self.y_data[:-1] = self.y_data[1:]
        self.y_data[-1] = np.random.rand()

        # Update the plot with new data
        self.plot.setData(self.x_data, self.y_data)


    def run(self):
        self.init_plot()
        self.start_timer()
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.run()
    sys.exit(app.exec_())

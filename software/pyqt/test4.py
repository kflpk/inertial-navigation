import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Plot with Legend")
        self.resize(800, 600)

        # Create a widget to hold the plot and legend
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create a layout to hold the plot and legend
        self.layout = QVBoxLayout(self.central_widget)

        # Create the plot widget
        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)

    def create_plot_with_legend(self):
        # Create a plot item
        plot_item = self.plot_widget.plotItem

        # Create curves
        curve1 = plot_item.plot(pen="r")
        curve2 = plot_item.plot(pen="g")
        curve3 = plot_item.plot(pen="b")

        # Add data to the curves
        x = [0, 1, 2, 3, 4]
        y1 = [0, 1, 2, 3, 4]
        y2 = [4, 3, 2, 1, 0]
        y3 = [2, 2, 2, 2, 2]

        curve1.setData(x, y1)
        curve2.setData(x, y2)
        curve3.setData(x, y3)

        # Create a legend widget
        legend_widget = QWidget()
        legend_layout = QVBoxLayout(legend_widget)

        # Add labels to the legend
        label1 = QLabel("Curve 1")
        label2 = QLabel("Curve 2")
        label3 = QLabel("Curve 3")

        legend_layout.addWidget(label1)
        legend_layout.addWidget(label2)
        legend_layout.addWidget(label3)

        # Add the legend widget to the layout
        self.layout.addWidget(legend_widget)

    def run(self):
        self.create_plot_with_legend()
        self.show()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.run()
    app.exec_()

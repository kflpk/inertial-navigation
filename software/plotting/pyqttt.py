import pyqtgraph.opengl as gl
import numpy as np
from PyQt5.QtWidgets import QApplication
import sys

# Create a QApplication instance
app = QApplication(sys.argv)

# Create an OpenGL widget
w = gl.GLViewWidget()

# Set the widget size
w.resize(800, 600)

# Set background color
w.setBackgroundColor('w')

# Create a grid
gx = gl.GLGridItem()
gy = gl.GLGridItem()
gz = gl.GLGridItem()
w.addItem(gx)
w.addItem(gy)
w.addItem(gz)

# Create a vector
start_point = np.array([0, 0, 0])  # Starting point of the vector
end_point = np.array([1, 2, 3])  # Ending point of the vector

# Create a line plot item
line_item = gl.GLLinePlotItem(pos=np.array([start_point, end_point]), color=(1, 0, 0, 1), width=3)

# Add the line item to the OpenGL widget
w.addItem(line_item)

# Show the widget
w.show()

# Start the Qt event loop
sys.exit(app.exec_())
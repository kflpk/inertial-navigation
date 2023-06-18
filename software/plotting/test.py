import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Initialize the figure and axis
fig, ax = plt.subplots()
x_data = np.linspace(0, 10, 100)  # x-axis data (assuming 100 points)

# Create an empty line object
line, = ax.plot([], [], color='b')

# Define the function to update the plot
def update_plot(frame):
    # Generate y-axis data for the frame
    y_data = np.sin(x_data + frame * 0.1)
    
    # Update the line data
    line.set_xdata(x_data)
    line.set_ydata(y_data)
    
    # Update the plot limits
    ax.set_xlim(0, 10)
    ax.set_ylim(-1, 1)

    # Redraw the canvas
    fig.canvas.draw()

# Create the animation
animation = FuncAnimation(fig, update_plot, frames=100, interval=16.6)

# Show the plot
plt.show()
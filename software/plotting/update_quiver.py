import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def my_function(i):
    ax.cla()
    ax.quiver(0, 0, 0, i/10000, i/10000, i/10000)

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ani = FuncAnimation(fig, my_function, interval=100)
plt.show()
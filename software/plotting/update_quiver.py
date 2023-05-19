import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

t = np.arange(0, 100, 0.01);
x = 15*np.cos(t)
y = 15*np.sin(t)
z = 15*np.tan(t)
_sample_no = -1
_sample_no2 = -1

def get_acc():
    global _sample_no
    _sample_no += 1
    return x[_sample_no], y[_sample_no], z[_sample_no]

def get_acc2():
    global _sample_no2
    _sample_no2 += 1
    return x[_sample_no2], y[_sample_no2], z[_sample_no2]

def update_3d(i):
    acc_ax.cla()
    x, y, z = get_acc()
    acc_ax.quiver(0, 0, 0, x, 0, 0);
    acc_ax.quiver(0, 0, 0, 0, y, 0);
    acc_ax.quiver(0, 0, 0, 0, 0, z);
    acc_ax.quiver(0, 0, 0, x, y, z, color='red');

    acc_ax.set_xlim(-15, 15)
    acc_ax.set_ylim(-15, 15)
    acc_ax.set_zlim(-15, 15)

    print(i)
    acc_ax.set_xlabel("X")
    acc_ax.set_ylabel("Y")
    acc_ax.set_zlabel("Z")
    acc_ax.set_title("siema")

fig = plt.figure()
acc_ax = fig.add_subplot(1, 2, 1, projection="3d")
vel_ax = fig.add_subplot(1, 2, 2)



ani1 = FuncAnimation(fig, update_3d, interval=10)
plt.show()
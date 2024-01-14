import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sensor import *

t = np.arange(0, 100, 0.01);
x = 15 * np.cos(10*t)
y = 15 * np.cos(10*t - 2 * np.pi / 3)
z = 15 * np.cos(10*t - 4 * np.pi / 3)
_sample_no  = -1
_sample_no2 = -1

at, ax, ay, az = [], [], [], []
mt, mx, my, mz = [], [], [], []
gt, gx, gy, gz = [], [], [], []

sensor = Sensor()

def get_acc():
    global _sample_no
    _sample_no += 1
    return x[_sample_no], y[_sample_no], z[_sample_no]

def get_acc2():
    global _sample_no2
    _sample_no2 += 1
    return _sample_no2, x[_sample_no2], y[_sample_no2], z[_sample_no2]

# def update_3d(i):
#     acc_ax.cla()
#     x, y, z = get_acc()
#     acc_ax.quiver(0, 0, 0, x, 0, 0);
#     acc_ax.quiver(0, 0, 0, 0, y, 0);
#     acc_ax.quiver(0, 0, 0, 0, 0, z);
#     acc_ax.quiver(0, 0, 0, x, y, z, color='red');

#     acc_ax.set_xlim(-15, 15)
#     acc_ax.set_ylim(-15, 15)
#     acc_ax.set_zlim(-15, 15)

#     acc_ax.set_xlabel("X")
#     acc_ax.set_ylabel("Y")
#     acc_ax.set_zlabel("Z")
#     acc_ax.set_title("siema")

def update_2d(i):
    global ax, ay, az
    buf_size = 30
   # ========== ACCELEROMETER ================ # 

    acc_2d.cla()
    acc_2d.grid(True)
    acc_2d.set_ylim(-20, 20)
    ts, x, y, z = sensor.get_acc()

    ax.append(x)
    ay.append(y)
    az.append(z)
    at.append(ts)

    if len(ax) == buf_size:
        ax.pop(0)
        ay.pop(0)
        az.pop(0)
        at.pop(0)

    acc_2d.plot(at, ax, label="X axis")
    acc_2d.plot(at, ay, label="Y axis")
    acc_2d.plot(at, az, label="Z axis")

    acc_2d.legend(loc='upper right')
    acc_2d.set_xlabel("Time")
    acc_2d.set_ylabel("Acc")
    acc_2d.set_title("Accelerometer")

    # ========== MAGNETOMETER =================

    mag_2d.cla()
    mag_2d.grid(True)
    mag_2d.set_ylim(-20, 20)
    ts, x, y, z = sensor.get_mag()

    mx.append(x)
    my.append(y)
    mz.append(z)
    mt.append(ts)

    if len(mx) == buf_size:
        mx.pop(0)
        my.pop(0)
        mz.pop(0)
        mt.pop(0)

    mag_2d.plot(mt, mx, label="X axis")
    mag_2d.plot(mt, my, label="Y axis")
    mag_2d.plot(mt, mz, label="Z axis")
    # line_mag_x.set_xdata(t)
    # line_mag_x.set_ydata(mx)
    # acc_2d.update()

    mag_2d.legend(loc='upper right')
    mag_2d.set_xlabel("Time")
    mag_2d.set_ylabel("Mag")
    mag_2d.set_title("Magnetometer")

    # ========== GYROSCOPE ===========

    gyro_2d.cla()
    gyro_2d.grid(True)
    gyro_2d.set_ylim(-20, 20)
    ts, x, y, z = sensor.get_gyro()

    gx.append(x)
    gy.append(y)
    gz.append(z)
    gt.append(ts)

    if len(gx) == buf_size:
        gx.pop(0)
        gy.pop(0)
        gz.pop(0)
        gt.pop(0)

    gyro_2d.plot(gt, gx, label="X axis")
    gyro_2d.plot(gt, gy, label="Y axis")
    gyro_2d.plot(gt, gz, label="Z axis")

    gyro_2d.legend(loc='upper right')
    gyro_2d.set_xlabel("Time")
    gyro_2d.set_ylabel("Gyro")
    gyro_2d.set_title("Gyroscope")

if __name__ == "__main__":
    fig = plt.figure()
    # acc_ax = fig.add_subplot(1, 2, 1, projection="3d")
    acc_2d  = fig.add_subplot(2, 2, 2)
    mag_2d  = fig.add_subplot(2, 2, 4)
    gyro_2d = fig.add_subplot(1, 2, 1)

    # line_mag_x, = mag_2d.plot([0, 1], [0,1], label="X axis")
    # line_mag_y, = mag_2d.plot([0, 1], [0,1], label="Y axis")
    # line_mag_z, = mag_2d.plot([0, 1], [0,1], label="Z axis")

    ani_acc3d = FuncAnimation(fig, update_3d, interval=10)
    # ani_acc2d = FuncAnimation(fig, update_2d, interval=16.6)

    plt.show()

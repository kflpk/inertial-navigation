import pandas as pd
import numpy as np
import math as m
import matplotlib.pyplot as plt
from ahrs.filters import Madgwick
from numpy import sin, cos

df = pd.read_csv("blok2.csv", sep=";")
time = df[["time"]].values
gFx = np.array(df['gFx'])* 9.81
gFy = np.array(df['gFy'])* 9.81
gFz = np.array(df['gFz'])* 9.81

wx = np.array(df['wx'])
wy = np.array(df['wy'])
wz = np.array(df['wz'])

Bx = np.array(df['Bx'])
By = np.array(df['By'])
Bz = np.array(df['Bz'])

sample_no = len(time)

pos_N = 0
pos_E = 0
positions_N = []
positions_E = []

vx = np.zeros(sample_no)
vy = np.zeros(sample_no)
vz = np.zeros(sample_no)
theta_acc = np.zeros(sample_no)
phi_acc = np.zeros(sample_no)
theta_gyro = np.zeros(sample_no)
phi_gyro = np.zeros(sample_no)
phi_dot = np.zeros(sample_no)
theta_dot = np.zeros(sample_no)
roll2 = np.zeros(sample_no)
pitch2 = np.zeros(sample_no)

alpha_filter = 0.02
g = 9.81
vx[0] = 0
vy[0] = 0
vz[0] = 0
phi_acc[0] = 0
theta_acc[0] = 0
phi_gyro[0] = 0
theta_gyro[0] = 0

i = 1
while i < sample_no:
    delta_t = abs(time[i] - time[i-1])
    vx[i] = vx[i - 1] + gFx[i] * (delta_t)
    vy[i] = vy[i - 1] + gFy[i] * (delta_t)
    vz[i] = vz[i - 1] + gFz[i] * (delta_t)
    i += 1


def euler_from_quaternion(x, y, z, w):  # getting roll pitch yaw from quaternions

        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = m.atan2(t0, t1)

        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = m.asin(t2)

        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = m.atan2(t3, t4)

        return roll_x, pitch_y, yaw_z  # in radians

roll = []
yaw = []
pitch = []
acc = 9.81 * df[["gFx", "gFy", "gFz"]].values
gyr = df[["wx", "wy", "wz"]].values
mag = 1000 * df[['Bx', 'By', 'Bz']].values

madgwick = Madgwick()
Q = np.tile((1., 0., 0., 0.), (len(gyr), 1))      # Allocation of quaternions
for t in range(0, sample_no):
    time_step = time[t] - time[t - 1]
    madgwick.Dt = time_step
    Q[t] = madgwick.updateMARG(Q[t - 1], gyr=gyr[t], acc=acc[t], mag=mag[t])
    roll, pitch, yaw = euler_from_quaternion(Q[t][1], Q[t][2], Q[t][3], Q[t][0])
    A = np.array([[cos(pitch)*cos(yaw), cos(pitch)*cos(yaw), -sin(pitch)],
                [-cos(roll)*sin(yaw)+sin(roll)*sin(pitch)*cos(yaw), cos(roll)*cos(yaw)+sin(roll)*sin(pitch)*sin(yaw), sin(roll)*cos(pitch)],
                [sin(roll)*sin(yaw)+cos(roll)*sin(pitch)*cos(yaw), -sin(roll)*cos(yaw)+cos(roll)*sin(pitch)*sin(yaw), cos(roll)*cos(pitch)]])
    a = np.array(acc[t]).T
    a_prim = A @ a
    pos_N = pos_N + (a_prim[0] * time_step ** 2) / 2
    pos_E = pos_E + (a_prim[1] * time_step ** 2) / 2
    positions_N.append(pos_N)
    positions_E.append(pos_E)


lw = 1
plt.subplot(4, 1, 1)
plt.plot(time, gFx, label="Axix X", linewidth=lw)
plt.plot(time, gFy, label="Axix Y", linewidth=lw)
plt.plot(time, gFz, label="Axix Z", linewidth=lw)
plt.legend()

plt.subplot(4, 1, 2)
plt.plot(time, wx, label="Axix X", linewidth=lw)
plt.plot(time, wy, label="Axix Y", linewidth=lw)
plt.plot(time, wz, label="Axix Z", linewidth=lw)
plt.legend()

plt.subplot(4, 1, 3)
plt.plot(time, Bx, label="Axix X", linewidth=lw)
plt.plot(time, By, label="Axix Y", linewidth=lw)
plt.plot(time, Bz, label="Axix Z", linewidth=lw)
plt.legend()

plt.subplot(4, 1, 4)
plt.scatter(positions_E,positions_N)
plt.show()
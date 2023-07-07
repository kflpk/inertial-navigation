import pandas as pd
import numpy as np
import math as m
import matplotlib.pyplot as plt
from ahrs.filters import Madgwick


df = pd.read_csv("ugabuga2.csv", sep=";")
time = np.array(df['time'])
gFx = - 9.809 * np.array(df['gFx'])
gFy = - 9.809 * np.array(df['gFy'])
gFz = - 9.809 * np.array(df['gFz'])

wx = np.array(df['wx'])
wy = np.array(df['wy'])
wz = np.array(df['wz'])

Bx = np.array(df['Bx'])
By = np.array(df['By'])
Bz = np.array(df['Bz'])

sample_no = len(time)

vx = np.zeros(sample_no)
vy = np.zeros(sample_no)
vz = np.zeros(sample_no)

vx[0] = 0
vy[0] = 0
vz[0] = 0

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
acc = df[["wx", "wy", "wz"]].values
gyr = df[["gFx", "gFy", "gFz"]].values
mag = df[['Bx', 'By', 'Bz']].values
#gyro_data = np.array[gFx, gFy, gFz]
#acc_data = np.array[wx, wy, wz]
#mag_data = np.array[Bx, By, Bz]
#np.seterr(invalid='ignore')

madgwick = Madgwick()
# Q = madgwick.Q
Q = np.tile((1., 0., 0., 0.), (len(gyr), 1))      # Allocation of quaternions
for t in range(0, sample_no):
   new_sample_rate = time[t] - time[t - 1]
   madgwick.Dt = new_sample_rate
   Q[t] = madgwick.updateMARG(Q[t - 1], gyr=gyr[t], acc=acc[t], mag=mag[t])
   x, y, z = euler_from_quaternion(Q[t][1], Q[t][2], Q[t][3],Q[t][0])
   pitch.append(y)
   yaw.append(z)
   roll.append(x)

shape = Q.shape
print(acc.shape)
print(gyr.shape)
print(mag.shape)
print(Q.shape)

print(euler_from_quaternion(0, 0, 0.707, 0.707))

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
plt.plot(time, roll, label="roll", linewidth=lw)
plt.plot(time, pitch, label="pitch", linewidth=lw)
plt.plot(time, yaw, label="yaw", linewidth=lw)
plt.legend()
plt.show()

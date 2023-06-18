import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

lw = 1

df = pd.read_csv("chodzenie po mieszkaniu.csv", sep=";")
time  = np.array(df['time'])
gFx  = np.array(df['gFx'])
gFy  = np.array(df['gFy'])
gFz  = np.array(df['gFz'])

wx  = np.array(df['wx'])
wy  = np.array(df['wy'])
wz  = np.array(df['wz'])

Bx  = np.array(df['Bx'])
By  = np.array(df['By'])
Bz  = np.array(df['Bz'])

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

plt.subplot(3, 1, 1)
plt.plot(time, gFx, label="Axix X", linewidth=lw)
plt.plot(time, gFy, label="Axix Y", linewidth=lw)
plt.plot(time, gFz, label="Axix Z", linewidth=lw)
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(time, wx, label="Axix X", linewidth=lw)
plt.plot(time, wy, label="Axix Y", linewidth=lw)
plt.plot(time, wz, label="Axix Z", linewidth=lw)
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(time, Bx, label="Axix X", linewidth=lw)
plt.plot(time, By, label="Axix Y", linewidth=lw)
plt.plot(time, Bz, label="Axix Z", linewidth=lw)
plt.legend()

plt.show()


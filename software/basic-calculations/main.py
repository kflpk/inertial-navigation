import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

lw = 1

df_prosto = pd.read_csv("chodzenie prosto.csv", sep=";")
time  = np.array(df_prosto['time'])
gFx  = np.array(df_prosto['gFx'])
gFy  = np.array(df_prosto['gFy'])
gFz  = np.array(df_prosto['gFz'])

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

plt.subplot(2, 1, 1)
plt.plot(time, gFx, label="Axix X", linewidth=lw)
plt.plot(time, gFy, label="Axix Y", linewidth=lw)
plt.plot(time, gFz, label="Axix Z", linewidth=lw)
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(time, vx, label="Axix X", linewidth=lw)
plt.plot(time, vy, label="Axix Y", linewidth=lw)
plt.plot(time, vz, label="Axix Z", linewidth=lw)

plt.show()


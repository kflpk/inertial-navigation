import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("dane.tsv", sep=',')
acc_x, acc_y, acc_z = df["acc_x"], df["acc_y"], df["acc_z"]
gyr_x, gyr_y, gyr_z = df["gyr_x"], df["gyr_y"], df["gyr_z"] 
mag_x, mag_y, mag_z = df["mag_x"], df["mag_y"], df["mag_z"] 
time = df["asyncio_time"]

plt.subplot(3, 1, 1)
plt.plot(time, acc_x)
plt.plot(time, acc_y)
plt.plot(time, acc_z)

plt.subplot(3, 1, 3)
plt.plot(time, gyr_x)
plt.plot(time, gyr_y)
plt.plot(time, gyr_z)

plt.subplot(3, 1, 2)
plt.plot(time, mag_x)
plt.plot(time, mag_y)
plt.plot(time, mag_z)


plt.show()
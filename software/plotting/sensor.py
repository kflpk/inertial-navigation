import time
import numpy as np
from scipy import signal

class Sensor:
    def __init__(self):
        self._initial_time = time.time()
        self.sampling_rate = 10

    def get_acc(self):
        now = time.time()
        delta_t = now - self._initial_time
        ax = 10 * np.sin(delta_t - 2 * np.pi / 3)
        ay = 10 * np.sin(delta_t - 4 * np.pi / 3)
        az = 10 * np.sin(delta_t)
        return delta_t, ax, ay, az

    def get_mag(self):
        now = time.time()
        delta_t = now - self._initial_time
        mx = 10 * signal.sawtooth(delta_t - 2 * np.pi / 3, 0.5)
        my = 10 * signal.sawtooth(delta_t - 4 * np.pi / 3, 0.5)
        mz = 10 * signal.sawtooth(delta_t                , 0.5)
        return delta_t, mx, my, mz
        

    def get_gyro(self):
        now = time.time()
        delta_t = now - self._initial_time
        gx = 10 * signal.square(delta_t - 2 * np.pi / 3)
        gy = 10 * signal.square(delta_t - 4 * np.pi / 3)
        gz = 10 * signal.square(delta_t                )
        return delta_t, gx, gy, gz

if __name__ == "__main__":
    sensor = Sensor()
    sensor.get_acc()
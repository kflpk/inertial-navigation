import numpy as np
import scipy.signal as signal
import random as random
from scipy.fft import fft


class Function_generator:
    def __init__(self, sampling_rate, timespan):
        self.sampling_rate = sampling_rate
        self.timespan = timespan
        self.time = np.linspace(0, timespan, timespan * sampling_rate)

    def sine(self, amplitude, frequency):
        return amplitude * np.sin(2 * np.pi * frequency * self.time)

    def square(self, amplitude, frequency):
        return amplitude * (np.sign(np.sin(2 * np.pi * frequency * self.time)))

    def sawtooth(self, amplitude, frequency):
        return signal.sawtooth(2 * np.pi * frequency * self.time) * amplitude

    def triangle(self, amplitude, frequency):
        return signal.sawtooth(2 * np.pi * frequency * self.time, 0.5) * amplitude

    def WhiteNoise(self, amplitude, frequency):
        return (np.random.rand(len(self.time)) - 0.5) * 2 * amplitude

    def fouriers_transform(t, y):
        N = len(t)
        dt = t[1] - t[0]
        yf = 2.0 / N * np.abs(fft(y)[0: N // 2])
        xf = np.fft.fftfreq(N, d=dt)[0: N // 2]
        return xf, yf

    def time_vector(self):
        return self.time

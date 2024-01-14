from scipy.fft import fft
import numpy as np
from generator import *
import pandas as pd
from scipy.io.wavfile import write
import scipy.signal as signal
import matplotlib.pyplot as plt


def fouriers_transform(t, y):
    N = len(t)
    dt = t[1] - t[0]
    yf = 2.0 / N * np.abs(fft(y)[0:N // 2])
    xf = np.fft.fftfreq(N, d=dt)[0:N // 2]
    print("fft done computin")
    return xf, yf

if __name__ == "__main__":
    while True:
        while True:  # Sampling rate
            try:
                sampling = int(input("Podaj częstotliwość próbkowania [Hz]:"))

                if sampling <= 0:
                    raise ValueError

                break
            except ValueError:
                print("Niepoprawna wartość, spróbuj ponownie")

        while True:  # Timespan
            try:
                timespan = int(input("Podaj czas trwania sygnału [s]:"))

                if timespan <= 0:
                    raise ValueError

                break
            except ValueError:
                print("Niepoprawna wartość, spróbuj ponownie")

        while True:  # X limit
            try:
                x_limit = float(input("Podaj zakres rysowania wykresu [s]:"))

                if x_limit <= 0:
                    raise ValueError

                break
            except ValueError:
                print("Niepoprawna wartość, spróbuj ponownie")

        while True:
            try:
                print("[1] Sine")
                print("[2] Square")
                print("[3] Sawtooth")
                print("[4] Triangle")
                print("[5] White noise")
                wav_num = input("Wybierz przebieg jaki chcesz wygenerować:")

                if (
                    wav_num != "1"
                    and wav_num != "2"
                    and wav_num != "3"
                    and wav_num != "4"
                    and wav_num != "5"
                ):
                    raise ValueError

                break
            except ValueError:
                print("Niepoprawna wartość, spróbuj ponownie")

        while True:  # Frequency
            try:
                if wav_num != "5":
                    frequency = float(input("Podaj częstotliwość sygnału [Hz]:"))
                    if frequency <= 0:
                        raise ValueError

                break
            except ValueError:
                print("Niepoprawna wartość, spróbuj ponownie")

        while True:  # Amplitude
            try:
                amplitude = float(input("Podaj amplitudę sygnału:"))

                if amplitude <= 0:
                    raise ValueError

                break
            except ValueError:
                print("Niepoprawna wartość, spróbuj ponownie")

        generator = Function_generator(sampling, timespan)

        if wav_num == "1":
            waveform_data = generator.sine(amplitude, frequency)
            waveform_title = "Sine: A = " + str(amplitude) + ", f = " + str(frequency)
        elif wav_num == "2":
            waveform_data = generator.square(amplitude, frequency)
            waveform_title = "Square: A = " + str(amplitude) + ", f = " + str(frequency)
        elif wav_num == "3":
            waveform_data = generator.sawtooth(amplitude, frequency)
            waveform_title = "Sawtooth: A = " + str(amplitude) + ", f = " + str(frequency)
        elif wav_num == "4":
            waveform_data = generator.triangle(amplitude, frequency)
            waveform_title = "Triangle: A = " + str(amplitude) + ", f = " + str(frequency)
        elif wav_num == "5":
            waveform_data = generator.WhiteNoise(amplitude)
            waveform_title = "White noise: A = " + str(amplitude)

        choice = input("Czy chcesz zapisać przegieg do pliku wav? [Y/n]:")
        if choice != "n" and choice != "N":
            filename = input("Podaj nazwę pliku wav:").strip()
            audio_data = np.int16(waveform_data * 2 ** 14)
            write(filename, sampling, audio_data)

        choice = input("Czy chcesz zapisać przegieg do pliku csv? [Y/n]:")
        if choice != "n" and choice != "N":
            filename = input("Podaj nazwę pliku csv:").strip()
            csv_data = {"t": generator.time, "v": waveform_data}
            dataframe = pd.DataFrame(csv_data)
            dataframe.to_csv(filename, index=False, sep="\t")

        fourier_freq, fourier_value = fouriers_transform(generator.time, waveform_data)

        fig, (waveform, fourier) = plt.subplots(2, 1)
        fig.subplots_adjust(hspace=0.8)

        waveform.set_xlabel("time (s)")
        waveform.set_ylabel("value")
        waveform.set_xlim(0, x_limit)
        waveform.title.set_text(waveform_title)
        waveform.plot(generator.time, waveform_data)

        fourier.set_xlabel("frequency (Hz)")
        fourier.set_ylabel("amplitude")
        fourier.title.set_text("Fourier's transform")
        fourier.plot(fourier_freq, fourier_value)

        plt.show()

        choice = input("Czy chcesz skorzystać z programu jeszcze raz? [Y/n]:")
        if choice == "n" or choice == "N":
            exit(0)

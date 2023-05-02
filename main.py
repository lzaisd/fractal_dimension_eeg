import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from scipy.signal import decimate

data = np.genfromtxt('file.asc', delimiter='\n')
# размер участка
# размер участка
window_size = 10000

# Perform the DWT
wavelet = 'db4'  # Adjust the wavelet as needed
level = 4  # Adjust the decomposition level as needed
coeffs = [data]
for _ in range(level):
    cA, cD = decimate(coeffs[-1], 2, zero_phase=True), np.zeros_like(coeffs[-1])
    cD[::2] = cA
    coeffs.append(cD)

# Calculate the wavelet spectrum
wavelet_spectrum = [np.sum(np.square(c)) for c in coeffs]

# размеры участков
sizes = [len(data) // (2 ** i) for i in range(level+1)]
# найти угол наклона графика
# найти угол наклона графика
slope, intercept = np.polyfit(np.log(sizes), np.log(wavelet_spectrum), 1)
# коэффициент самоподобия
fractal_dimension = slope
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(filetypes=[("ASC files", "*.asc")])

# считать данные из файла
f = open(file_path, 'r')
data = np.genfromtxt(f, delimiter='\n')
f.close()

# построить графики
fig, axs = plt.subplots(2)
fig.suptitle('Коэффициент самоподобия ЭЭГ')

# построить график ЭЭГ
axs[0].plot(data)
axs[0].set_xlim([5000, 214000])
# построить график зависимости логарифма дисперсии от логарифма размера участков
axs[1].plot(np.log(sizes), np.log(wavelet_spectrum))
axs[1].plot(np.log(sizes), slope * np.log(sizes) + intercept, color='red', label='Аппроксимирующая линия')
axs[1].set_xlim([9.5, 12.274])
axs[1].set_xlabel('Log(размера окна)')
axs[1].set_ylabel('Log(вейвлет спектра)')
axs[1].set_title('Коэффициент самоподобия = ' + str(round(fractal_dimension, 6)))
axs[1].legend()

plt.show()

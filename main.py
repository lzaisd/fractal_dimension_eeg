import math
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from scipy.signal import cwt, ricker
from scipy.signal import butter, filtfilt

# считать данные из файла
file_path = filedialog.askopenfilename(filetypes=[("ASC files", "*.asc")])
f = open(file_path, 'r')
data = np.genfromtxt(f, delimiter='\n')
f.close()
# фильтрация
cutoff_freq = 100
sampling_rate = 500
normalized_cutoff_freq = cutoff_freq / (0.5 * sampling_rate)
b, a = butter(4, normalized_cutoff_freq, btype='low', analog=False)
data = filtfilt(b, a, data)
# размер участка
window_size = 10000
# Calculate the wavelet spectrum using Continuous Wavelet Transform (CWT)
widths = np.arange(1, 10)
cwt_matrix = cwt(data, ricker, widths)
# размеры участков
sizes = [len(data) // (2 ** i) for i in range(len(widths))]
# найти угол наклона графика
slope, intercept = np.polyfit(np.log(sizes), np.log(np.sum(np.abs(cwt_matrix), axis=1)), 1)
# коэффициент самоподобия
fractal_dimension = slope
root = tk.Tk()
root.withdraw()
# построить графики
fig, axs = plt.subplots(3)
fig.suptitle('Коэффициент самоподобия ЭЭГ')

# построить график ЭЭГ
axs[0].plot(data)
#axs[0].set_xlim([5000, 214000])
# построить график вейвлет спектра
im = axs[1].imshow(np.abs(cwt_matrix), extent=[0, len(data), widths[-1], widths[0]], aspect='auto', cmap='jet')
axs[1].set_title('Вейвлет спектр')
fig.colorbar(im, ax=axs[1], label='Амплитуда')
# построить график зависимости логарифма суммы модулей вейвлет спектра от логарифма размера участков
axs[2].plot(np.log(sizes), np.log(np.sum(np.abs(cwt_matrix), axis=1)))
axs[2].plot(np.log(sizes), slope * np.log(sizes) + intercept, color='red', label='Аппроксимирующая линия')
#axs[2].set_xlim([9.5, 12.274])
axs[2].set_xlabel('Log(размера окна)')
axs[2].set_ylabel('Log(вейвлет спектра)')
axs[2].set_title('Коэффициент самоподобия = ' + str(round(math.tan(fractal_dimension), 6)))
axs[2].legend()

plt.show()

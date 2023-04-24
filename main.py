import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

data = np.genfromtxt('file.asc', delimiter='\n')
# размер участка
window_size = 10000
# разбить сигнал на участки
windows = [data[i:i+window_size] for i in range(0, len(data), window_size)]
# вычислить дисперсию для каждого участка
variances = [np.var(window) for window in windows]
# размеры участков
sizes = [len(window) for window in windows]
# построить график зависимости логарифма дисперсии от логарифма размера участков
# plt.plot(np.log(sizes), np.log1p(variances))
# plt.xlabel('Log(Window size)')
# plt.ylabel('Log(Variance)')
# plt.show()
# найти угол наклона графика
slope, intercept = np.polyfit(np.log(sizes), np.log1p(variances), 1)
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
axs[0].set_xlim([0, 214000])
# построить график зависимости логарифма дисперсии от логарифма размера участков
window_size = 10000
windows = [data[i:i+window_size] for i in range(0, len(data), window_size)]
sizes = [len(window) for window in windows]
variances = [np.var(window) for window in windows]
axs[1].plot(np.log(sizes), np.log1p(variances))
axs[1].set_xlabel('Log(размера окна)')
axs[1].set_ylabel('Log(дисперсии)')
axs[1].set_title('Коэффициент самоподобия = ' + str(round(fractal_dimension, 6)))
axs[1].set_xlim([8.292, 9.190])

plt.show()
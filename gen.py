import numpy as np

# Set the parameters
amplitude = 100.0  # Amplitude of the sine wave
frequency = 30.0  # Frequency of the sine wave
num_samples = 5000  # Number of samples in the sine wave

# Generate the time axis
time = np.linspace(0, 1, num_samples)

# Generate the sine wave
sine_wave = amplitude * np.sin(2 * np.pi * frequency * time)

# Write the values to a file
file_path = 'sine_wave.asc'  # Specify the file path
with open(file_path, 'w') as file:
    for value in sine_wave:
        file.write(f'{value}\n')
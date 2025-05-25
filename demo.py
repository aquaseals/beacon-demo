import numpy as np
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt

from scipy.io import wavfile
from IPython.display import Audio
from IPython.core.display import HTML
import sounddevice as sd

# Set the backend to 'Agg' (non-interactive) or 'TkAgg' (interactive)
# For Codespaces, use 'Agg' and save the plot to a file or use inline magic if in a notebook.
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend (saves to file)
# OR for Jupyter-like display (if using a notebook in Codespaces):
# %matplotlib inline

def play_audio(signal, sample_rate):
    """
    Play audio from a NumPy array.
    Args:
        signal (np.array): Audio signal (e.g., sine wave).
        sample_rate (int): Sampling rate in Hz.
    """
    # Normalize to 16-bit PCM format (-1 to 1 range)
    signal_normalized = np.int16(signal * (32767 / np.max(np.abs(signal))))
    sd.play(signal_normalized, sample_rate)
    sd.wait()  # Wait until playback finishes


input_audio = wavfile.read("Tokyo Rain Serenade.wav")
sample_rate = input_audio[0]

channel_0 = input_audio[1][:, 0]
audio = np.array(channel_0, dtype=np.float64) / np.max(channel_0)

play_audio(audio, sample_rate)


'''# Generate signal
sr = 2000  # Sample rate
ts = 5.0 / sr  # Sample interval
t = numpy.arange(0, 1, ts)  # Time vector
freq = 500  # Frequency (Hz)
x = 3 * numpy.sin(2 * numpy.pi * freq * t)  # Signal

# Compute FFT
N = len(x)
yf = fft(x)
xf = fftfreq(N, ts)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(xf, numpy.abs(yf))
plt.title('FFT of Sine Wave')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.grid()

# Save the plot to a file (since 'Agg' backend doesn't display interactively)
plt.savefig('fft_plot.png')
print("Plot saved as 'fft_plot.png'")

# Alternative: Display in-line (if using a Jupyter notebook in Codespaces)
#plt.show()  # Uncomment if using %matplotlib inline'''
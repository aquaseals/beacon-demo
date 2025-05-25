import numpy as np
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt

from scipy.io import wavfile
import sounddevice as sd

'''
amplitude -> volume of a sound, specifically the wave sample of that sound
frequency -> pitch of a sound, # of sound wave oscillations per second

'''

def play_audio(signal, sample_rate):
    #takes floting point # and turns it back into audio waveform samples
    signal_normalized = np.int16(signal * (32767 / np.max(np.abs(signal)))) 
    #plays that audio waveform sample at the given sample rate (frequency, hz) one at a time -> multiple samples strung together make the sound
    sd.play(signal_normalized, sample_rate) 
    # wait until playback finishes
    sd.wait()  

# return (sample_rate and audio data)
input_audio = wavfile.read("Tokyo Rain Serenade.wav")
# how many samples per second
sample_rate = input_audio[0] 
print(sample_rate)

channel_0 = input_audio[1][:, 0]
# converts audio data (repped by long range of #) into managable floating point # between the smallest and largest data # (e.x. if 0.9m is the highest amplitude sample, that becomes 1)
# specifically extracts only the left channel (appplicable to stereo or headphones for example) -> explains why when playing the sound it no longer has that dimension?
audio = np.array(channel_0, dtype=np.float64) / np.max(channel_0)

#play_audio(audio, sample_rate)
#computes floting point # representation of sample into complex coeffcients (coefficienct represents how loud a specific frequency is -> amplitude, when frequency starts in the sequence of samples)
fourier_coefficients = np.fft.rfft(audio, norm="forward")
frequency_spectrum =  np.fft.rfftfreq(len(audio), 1 / sample_rate)

plt.figure(figsize=(20, 5))
plt.plot(frequency_spectrum, fourier_coefficients.real)
plt.xlabel("frequency (hz)", fontsize=14)

plt.savefig('fft_plot.png')
print("Plot saved as 'fft_plot.png'")
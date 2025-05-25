import numpy as np
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt

from scipy.io import wavfile
import sounddevice as sd
from scipy.io.wavfile import write

from pynput.keyboard import Listener

'''
amplitude -> volume of a sound, specifically the wave sample of that sound
frequency -> pitch of a sound, # of sound wave oscillations per second

'''

def play_audio(signal, sample_rate):
    #takes floating point # and turns it back into audio waveform samples
    signal_normalized = np.int16(signal * (32767 / np.max(np.abs(signal)))) 
    #plays that audio waveform sample at the given sample rate (frequency, hz) one at a time -> multiple samples strung together make the sound
    sd.play(signal_normalized, sample_rate) 
    # wait until playback finishes
    sd.wait()  

def lowpass_filter(frequencies, spectrum, max_freq):
    """A lowpass filter. 
    
    Filter out the parts of the spectrum above the specified frequency.
    
    Args:
        frequencies (array[float]): The frequencies of the Fourier coefficients
            (in Hz, obtained from np.fft.rfftfreqs).
        spectrum (array[complex]): The Fourier coefficients obtained by applying
            the FFT to an audio signal.
        max_freq (float): The maximum frequency, in Hz, allowed by the lowpass filter.
        
    Returns:
        array[complex]: A modified spectrum containing only the Fourier coefficients
        up to the specified frequency.
    """
    spectrum2 = np.array(spectrum)
    #going through each frequency of each fourier tranform coefficient and comparing to max frequency filter, if higher, setting the coefficient to 0 to modify the recorded occurence of a frequency 
    for idx, val in np.ndenumerate(frequencies):
        if val >= max_freq:
            spectrum2[idx] = 0
    return spectrum2

def highpass_filter(frequencies, spectrum, min_freq):
    """A highpass filter. 
    
    Filter out the parts of the spectrum below the specified frequency.
    
    Args:
        frequencies (array[float]): The frequencies of the Fourier coefficients
            (in Hz, obtained from np.fft.rfftfreqs).
        spectrum (array[complex]): The Fourier coefficients obtained by applying
            the FFT to an audio signal.
        min_freq (float): The minimum frequency, in Hz, allowed by the highpass filter.
        
    Returns:
        array[complex]: A modified spectrum containing only the Fourier coefficients
        above the specified frequency. 
    """
    spectrum3 = np.array(spectrum)
    #going through each frequency of each fourier tranform coefficient and comparing to max frequency filter, if higher, setting the coefficient to 0 to modify the recorded occurence of a frequency 
    for idx, val in np.ndenumerate(frequencies):
        if val <= min_freq:
            spectrum3[idx] = 0
    return spectrum3

def bandpass_filter(frequencies, spectrum, min_freq, max_freq):
    """A bandpass filter. 
    
    Keep only the parts of the frequency spectrum in a given range.
    
    Args:
        frequencies (array[float]): The frequencies of the Fourier coefficients
            (in Hz, obtained from np.fft.rfftfreqs).
        spectrum (array[complex]): The Fourier coefficients obtained by applying
            the FFT to an audio signal.
        min_freq (float): The minimum frequency, in Hz, allowed by the bandpass filter.
        max_freq (float): The maximum frequency, in Hz, allowed by the bandpass filter.
        
    Returns:
        array[complex]: A modified spectrum containing only the Fourier coefficients
        within the given frequency band. 
    """
    spectrum4 = highpass_filter(frequencies, spectrum, min_freq)
    spectrum5 = lowpass_filter(frequencies, spectrum4, max_freq)

       
    return spectrum5


def bandstop_filter(frequencies, spectrum, min_freq, max_freq):
    """A bandstop filter. 
    
    Remove parts of the frequency spectrum in a given range.
    
    Args:
        frequencies (array[float]): The frequencies of the Fourier coefficients
            (in Hz, obtained from np.fft.rfftfreqs).
        spectrum (array[complex]): The Fourier coefficients obtained by applying
            the FFT to an audio signal.
        min_freq (float): The lowest frequency, in Hz, stopped by the filter.
        max_freq (float): The highest frequency, in Hz, stopped by the filter.
        
    Returns:
        array[complex]: A modified spectrum containing only the Fourier coefficients
        outside the given frequency band. 
    """
    
    spectrum7 = highpass_filter(frequencies, spectrum, max_freq)
    spectrum6 = lowpass_filter(frequencies, spectrum, min_freq)
    
    return spectrum6+spectrum7

def containsFrequency(frequencies, spectrum, min_freq, max_freq):
    spectrum = bandpass_filter(frequencies, spectrum, min_freq, max_freq)
    for f in spectrum:
        # checking if floating point # after filteration are greater than 0, used floating point decimal for better accuracy
        if f > 0.001:
            return True

    return False

def on_press(key):
    if key == 'r':
        #creating 5 sec recording w/ microphone
        print("recording starting")
        fs = 44100
        seconds = 5
        recorded = sd.rec(int(seconds*fs), samplerate=fs, channels=2)
        sd.wait()
        write('recording.wav', fs, recorded)
        print("recording done")

        # return (sample_rate and audio data) from recorded .wav file
        input_audio = wavfile.read("recording.wav")
        # how many samples per second
        sample_rate = input_audio[0] 

        channel_0 = input_audio[1][:, 0]
        # converts audio data (repped by long range of #) into managable floating point # between the smallest and largest data # (e.x. if 0.9m is the highest amplitude sample, that becomes 1)
        # specifically extracts only the left channel (appplicable to stereo or headphones for example) -> explains why when playing the sound it no longer has that dimension?
        audio = np.array(channel_0, dtype=np.float64) / np.max(channel_0)

        #play_audio(audio, sample_rate) ignore this line
        #computes floating point # representation of sample into complex coeffcients (coefficienct represents how loud a specific frequency is -> amplitude, when frequency starts in the sequence of samples)
        fourier_coefficients = np.fft.rfft(audio, norm="forward")
        frequency_spectrum =  np.fft.rfftfreq(len(audio), 1 / sample_rate)

        #adjust frquencies here
        medical = 250
        rescue = 625
        supplies = 440

        med_signals = containsFrequency(frequency_spectrum, fourier_coefficients.real, medical-25, medical+25)
        res_signals = containsFrequency(frequency_spectrum, fourier_coefficients.real, rescue-25, rescue+25)
        supply_signals = containsFrequency(frequency_spectrum, fourier_coefficients.real, supplies-25, supplies+25)
        
        if med_signals == True: 
            print("medical supplies signal recieved")
        if res_signals == True: 
            print("rescue signal recieved")
        if supply_signals == True: 
            print("resources signal recieved")

        '''
        cool stuff but irrelevant
        #fig 1
        plt.figure(figsize=(5, 5))
        plt.plot(frequency_spectrum, bandpass_filter(frequency_spectrum, fourier_coefficients.real, medical-5, medical+5))
        plt.xlabel("frequency (hz)", fontsize=14)

        plt.savefig('fig1.png')

        #fig 2
        plt.figure(figsize=(5, 5))
        plt.plot(frequency_spectrum, bandpass_filter(frequency_spectrum, fourier_coefficients.real, rescue-5, rescue+5))
        plt.xlabel("frequency (hz)", fontsize=14)

        plt.savefig('fig2.png')

        #fig 3
        plt.figure(figsize=(5, 5))
        plt.plot(frequency_spectrum, bandpass_filter(frequency_spectrum, fourier_coefficients.real, supplies-5, supplies+5))
        plt.xlabel("frequency (hz)", fontsize=14)

        plt.savefig('fig3.png')

        #fig 4
        plt.figure(figsize=(10, 5))
        plt.plot(audio)
        plt.xlabel("frequency (hz)", fontsize=14)

        plt.savefig('fig4.png')'''


while True:
    key = input("type a button: ")
    on_press(key)
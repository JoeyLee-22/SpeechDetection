import numpy as np
import matplotlib.pyplot as plt
from math import ceil
from scipy.io.wavfile import write
from scipy.io.wavfile import read
import azure.cognitiveservices.speech as speechsdk

def demo_grapher(a, snr, scores):
    alpha = 0.45
    s = 10
    
    plt.scatter(a, scores, color='blue', alpha=alpha, s=s)
    plt.title("a vs. score")
    plt.xlabel("a")
    plt.ylabel("score")
    plt.xticks(np.arange(min(a), max(a)+0.5, .5))
    plt.yticks(np.arange(min(scores), max(scores)+0.1, .1))
    plt.show()

def grapher(s, n, a, snr, S1, S1_prime):
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True

    plt.plot(s, color='blue')
    plt.plot(n, color='red', alpha=0.65)

    plt.ylabel("Amplitude")
    plt.xlabel("Time")
    plt.title(f"a: {a:.2f}, SNR: {snr}\nS1: {S1}\nS1': {S1_prime}")
    plt.show()




    # sample_rate = 44100
    # length_in_seconds = ceil(s.shape[0]/sample_rate)
    # n = np.random.normal(-1, 1, sample_rate * length_in_seconds)
    # # n = np.random.uniform(-1, 1, sample_rate * length_in_seconds)
    # write('audio/test_n.wav', sample_rate, n)
    # s = np.append(s, [0]*(length_in_seconds*sample_rate - s.shape[0])) 
    
    # y = fft(n)
    # y = 0.0005*s+0.02*n[:s.shape[0]]
    # # y = 0.0005*s-0.0004999999*s
    # write('audio/test_combined.wav', samplerate_s, y)

    # print(recognize_from_file(speechsdk.audio.AudioConfig(filename="audio/test_combined.wav")))
    # plt.plot(s, color='blue')

    # plt.ylabel("Amplitude")
    # plt.xlabel("Time")
    # plt.show()
    
    # plt.plot(n, color='red')

    # plt.ylabel("Amplitude")
    # plt.xlabel("Time")
    # plt.show()
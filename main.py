import os
import json
import numpy as np
import azure.cognitiveservices.speech as speechsdk
import string
from wavImEx import import_wave_file, export_wave_file
from graphs import grapher, demo_grapher
from getData import get_data
from getScore import get_score
from normalization import rms
from speechToText import get_text
from scipy.io.wavfile import write
from datetime import datetime

with open('config.json', 'r') as f:
    config = json.load(f)
log_folder = config["log_folder"]

if (config["demo_mode"]):
    a, snr, S1, S1_prime, scores = get_data(log_folder)
    demo_grapher(a, snr, scores)
else:
    a_start = config["sweep_start"]
    a_end = config["sweep_end"]
    a = a_start
    is_logging = config["is_logging"]
    is_graphing = config["is_graphing"]
    sampling_rate = 44100
    k = range(config["sentence_start_sec"]*sampling_rate, config["sentence_end_sec"]*sampling_rate)

    s = import_wave_file("audio/long_sentence.wav")[k]
    n = import_wave_file("audio/whiteNoise.wav")[k]

    s_norm = s/rms(s)
    n_norm = n/rms(n)

    export_wave_file("audio/S1.wav", s_norm, sampling_rate)
    S1 = get_text(speechsdk.audio.AudioConfig(filename="audio/S1.wav"))

    path = "audio"
    counter = 0
    while(True):
        s_prime = s_norm + a*n_norm
        
        try:
            snr_full = (rms(s_norm)/rms(a*n_norm))**2
            snr_theory = 1/(a**2)
            snr = f"{snr_full:.2f}"
            snr_full = f"{snr_full:.5f}"
        except:
            snr = 'NA'
            snr_full = 'NA'
            snr_theory = 'NA'
        if (is_logging):
            date_time = datetime.now().strftime("%m-%d,%H:%M:%S")
            path = f"{log_folder}/{date_time},a={a:.2f},SNR={snr}"
            os.mkdir(path)

        export_wave_file(f"{path}/s_prime.wav", s_prime, sampling_rate)
        S1_prime = get_text(speechsdk.audio.AudioConfig(filename=f"{path}/s_prime.wav"))
        score = get_score([S1.lower().translate(str.maketrans('', '', string.punctuation))], [S1_prime.lower().translate(str.maketrans('', '', string.punctuation))])[0]
        
        export_wave_file(f"{path}/s_norm.wav", s_norm, sampling_rate)
        export_wave_file(f"{path}/s.wav", s, sampling_rate)
        export_wave_file(f"{path}/n_norm.wav", n_norm, sampling_rate)
        export_wave_file(f"{path}/n.wav", n, sampling_rate)
        export_wave_file(f"{path}/a*n_norm.wav", a*n_norm, sampling_rate)
        
        f = open(f"{path}/results.txt", "w")
        f.write(f"{a:.5f}\n{snr_full}\n{S1}\n{S1_prime}\n{score}")
        f.close()
        
        print(f'a: {a:.5f}, SNR: {snr}, SNR THEORY: {snr_theory}')
        if (score == 0):
            counter+=1
        else:
            counter=0
        print(f"S1 : {S1}")
        print(f"S1': {S1_prime}")
        print(f"Score: {score:.5f}\n")
        
        a += 0.1
        if (a > a_end or counter==1):
            break
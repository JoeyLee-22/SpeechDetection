import os
import json
import joblib
import time
import numpy as np
from math import floor
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from graphs import demo_grapher_mf
from getData import get_data_mf
from computeMFCC import compute_mfcc

with open('config.json', 'r') as f:
        config = json.load(f)

model_filename = config["model_filename"]
audio_filename = config["audio_filename"]
n_mfcc = config["n_mfcc"]
n_fft = config["n_fft"]
hop_length = config["hop_length"]

if (config["demo_mode"] and config["load_model"]):
    loaded_model = joblib.load(model_filename)
    
    print("LOADING DATA...")
    start = time.time()
    a, snr, S1, S1_prime, scores = get_data_mf("logV7", loaded_model, n_mfcc, n_fft, hop_length)
    total_time = time.time() - start
    hours = floor(total_time/3600)
    minutes = floor((total_time - hours*3600)/60)
    seconds = floor(total_time - hours*3600 - minutes*60)
    print(f"DATA LOADED\nTIME TAKEN: {hours:02d}:{minutes:02d}:{seconds:02d}")
    
    demo_grapher_mf(a, snr, scores)

else: 
    if (config["train_model"]):
        path = "mfModelTrainingData"
        speech_files = []
        non_speech_files = []

        for subdir, dirs, files in os.walk(path):
            for file in files:
                if (file == "s_norm.wav"):
                    speech_files.append(os.path.join(subdir, file))
                elif (file == "a*n_norm.wav"):
                    non_speech_files.append(os.path.join(subdir, file))
        speech_features = [compute_mfcc(file, n_mfcc, n_fft, hop_length) for file in speech_files]
        non_speech_features = [compute_mfcc(file, n_mfcc, n_fft, hop_length) for file in non_speech_files]

        speech_features = np.concatenate(speech_features, axis=1).T
        non_speech_features = np.concatenate(non_speech_features, axis=1).T

        speech_labels = np.ones(len(speech_features))
        non_speech_labels = np.zeros(len(non_speech_features))

        X = np.vstack((speech_features, non_speech_features))
        y = np.hstack((speech_labels, non_speech_labels))

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        print(f"MODEL NAME: {model_filename}")
        print(f"n_mfcc:{n_mfcc}\tn_fft:{n_fft}\thop_length:{hop_length}")
        print("\nTRAINING SVM CLASSIFIER...")
        start = time.time()
        svm_classifier = SVC(kernel='linear')
        svm_classifier.fit(X_train, y_train)
        print("SVM CLASSIFIER TRAINING FINISHED")
        total_time = time.time() - start
        hours = floor(total_time/3600)
        minutes = floor((total_time - hours*3600)/60)
        seconds = floor(total_time - hours*3600 - minutes*60)
        print(f"TRAINING TIME: {hours:02d}:{minutes:02d}:{seconds:02d}")

        predictions = svm_classifier.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)
        print("\nTEST SET ACCURACY:", accuracy)

    if (config["train_model"] and config["save_model"]):
        print("\nSAVING MODEL...")
        joblib.dump(svm_classifier, model_filename)
        print("MODEL SAVED\n")

    if (config["predict"]):
        new_features = compute_mfcc(audio_filename, n_mfcc, n_fft, hop_length)
        
        if (config["load_model"]):
            loaded_model = joblib.load(model_filename)
            prediction = loaded_model.predict(new_features.T)
        else:
            prediction = svm_classifier.predict(new_features.T)
            
        zero_counter = 0
        for num in prediction:
            if num == 0:
                zero_counter+=1
        
        print(f"Model Used: {model_filename}")
        print(f"Audio File: {audio_filename}")
        print(f"\nPrediction Variables\nn_mfcc: {n_mfcc}\nn_fft: {n_fft}\nhop_length: {hop_length}")
        print(f"\nPrediction Length: {prediction.size}")
        print(f"Y P/I Hops: {prediction.size - zero_counter}")
        print(f"N P/I Hops: {zero_counter}")
        
        avg = np.average(prediction)
        print(f"\nP/I: {avg*100:.3f}%")

# import os
# import json
# import joblib
# import time
# import numpy as np
# from math import floor
# from sklearn.svm import SVC
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
# from graphs import demo_grapher_mf
# from getData import get_data_mf
# from computeMFCC import compute_mfcc
# from processSaveData import getPIDataArr

# with open('config.json', 'r') as f:
#         config = json.load(f)

# model_filename = config["model_filename"]
# audio_filename = config["audio_filename"]
# n_mfcc = config["n_mfcc"]
# n_fft = config["n_fft"]
# hop_length = config["hop_length"]

# if (config["demo_mode"] and config["load_model"]):
#     loaded_model = joblib.load(model_filename)
    
#     print("LOADING DATA...")
#     start = time.time()
#     a, snr, S1, S1_prime, scores = get_data_mf("logV7", loaded_model, n_mfcc, n_fft, hop_length)
#     total_time = time.time() - start
#     hours = floor(total_time/3600)
#     minutes = floor((total_time - hours*3600)/60)
#     seconds = floor(total_time - hours*3600 - minutes*60)
#     print(f"DATA LOADED\nTIME TAKEN: {hours:02d}:{minutes:02d}:{seconds:02d}")
    
#     demo_grapher_mf(a, snr, scores)

# else: 
#     if (config["train_model"]):
#         path = "mfModelTrainingData2"
#         data_array = getPIDataArr('PIData.txt')
#         type_dict = {"bottom":0, "front":1, "rear":2}
#         speech_files = []
#         speech_labels = []

#         for filename in os.listdir(path):
#             f = os.path.join(path, filename)
#             speech_files.append(f)
            
#             info = f.split("_")
#             type = info[0][21:]
#             decibel_lvl = int(info[1][0:2])
#             row = int(info[2][2:3])
#             for i in range(330):
#                 if row==0:
#                     row_num = row*3+type_dict[type]
#                 else:
#                     row_num = row*3+type_dict[type]-15
#                 speech_labels.append(data_array[row_num][int((decibel_lvl-70)/5)])
        
#         speech_labels = np.asarray(speech_labels)
#         speech_features = [compute_mfcc(file, n_mfcc, n_fft, hop_length) for file in speech_files]
#         speech_features = np.concatenate(speech_features, axis=1).T
        
#         X = speech_features
#         y = speech_labels

#         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#         print(f"MODEL NAME: {model_filename}")
#         print(f"n_mfcc:{n_mfcc}\tn_fft:{n_fft}\thop_length:{hop_length}")
#         print("\nTRAINING SVM CLASSIFIER...")
#         start = time.time()
#         svm_classifier = SVC(kernel='linear')
#         svm_classifier.fit(X_train, y_train)
#         print("SVM CLASSIFIER TRAINING FINISHED")
#         total_time = time.time() - start
#         hours = floor(total_time/3600)
#         minutes = floor((total_time - hours*3600)/60)
#         seconds = floor(total_time - hours*3600 - minutes*60)
#         print(f"TRAINING TIME: {hours:02d}:{minutes:02d}:{seconds:02d}")

#         predictions = svm_classifier.predict(X_test)

#         accuracy = accuracy_score(y_test, predictions)
#         print("\nTEST SET ACCURACY:", accuracy)

#     if (config["train_model"] and config["save_model"]):
#         print("\nSAVING MODEL...")
#         joblib.dump(svm_classifier, model_filename)
#         print("MODEL SAVED\n")

#     if (config["predict"]):
#         new_features = compute_mfcc(audio_filename, n_mfcc, n_fft, hop_length)
        
#         if (config["load_model"]):
#             loaded_model = joblib.load(model_filename)
#             prediction = loaded_model.predict(new_features.T)
#         else:
#             prediction = svm_classifier.predict(new_features.T)
                
#         prediction = [i * 0.25 for i in prediction]
        
#         zero_counter = 0
#         for num in prediction:
#             if num == 0:
#                 zero_counter+=1
        
#         print(f"Model Used: {model_filename}")
#         print(f"Audio File: {audio_filename}")
#         print(f"\nPrediction Variables\nn_mfcc: {n_mfcc}\nn_fft: {n_fft}\nhop_length: {hop_length}")
#         print(f"\nPrediction Length: {len(prediction)}")
#         print(f"Y P/I Hops: {len(prediction) - zero_counter}")
#         print(f"N P/I Hops: {zero_counter}")
        
#         avg = np.average(prediction)
#         print(f"\nP/I: {avg*100:.3f}%")
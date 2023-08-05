import librosa
import os
import json
import joblib
import time
import numpy as np
from math import floor
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def compute_mfcc(audio_file, n_mfcc=13, n_fft=2048, hop_length=128):
    y, sr = librosa.load(audio_file)
    mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length)
    mfccs = librosa.feature.mfcc(S=librosa.power_to_db(mel_spec), n_mfcc=n_mfcc)
    return mfccs

def train_model(model_filename):
    path = "mfModelTrainingData"
    speech_files = []
    non_speech_files = []

    for subdir, dirs, files in os.walk(path):
        for file in files:
            if (file == "s_norm.wav"):
                speech_files.append(os.path.join(subdir, file))
            elif (file == "a*n_norm.wav"):
                non_speech_files.append(os.path.join(subdir, file))
    speech_features = [compute_mfcc(file) for file in speech_files]
    non_speech_features = [compute_mfcc(file) for file in non_speech_files]

    speech_features = np.concatenate(speech_features, axis=1).T
    non_speech_features = np.concatenate(non_speech_features, axis=1).T

    speech_labels = np.ones(len(speech_features))
    non_speech_labels = np.zeros(len(non_speech_features))

    X = np.vstack((speech_features, non_speech_features))
    y = np.hstack((speech_labels, non_speech_labels))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("TRAINING SVM CLASSIFIER...")
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

    print("\nSAVING MODEL...")
    joblib.dump(svm_classifier, model_filename)
    print("MODEL SAVED")

def load_and_predict(model_filename, new_audio_file):
    loaded_model = joblib.load(model_filename)

    new_features = compute_mfcc(new_audio_file)

    prediction = loaded_model.predict(new_features.T)
    
    zero_counter = 0
    for num in prediction:
        if num == 0:
            zero_counter+=1
    
    print(f"Model Used: {model_filename}")
    print(f"Audio File: {new_audio_file}")
    print(f"\nPrediction Length {prediction.size}")
    print(f"Y Presence Hops: {prediction.size - zero_counter}")
    print(f"N Presence Hops: {zero_counter}")
    
    avg = np.average(prediction)
    print(f"\nPresence: {avg*100:.3f}%")

if __name__ == "__main__":
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    model_filename = config["model_filename"]
    audio_filename = config["audio_filename"]
    
    if (config["train"]):
        train_model(model_filename)
    
    if (config["load_and_predict"]):
        load_and_predict(model_filename, audio_filename)
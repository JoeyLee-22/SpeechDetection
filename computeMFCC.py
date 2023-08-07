import librosa

def compute_mfcc(audio_file, n_mfcc, n_fft, hop_length):
    y, sr = librosa.load(audio_file)
    mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length)
    mfccs = librosa.feature.mfcc(S=librosa.power_to_db(mel_spec), n_mfcc=n_mfcc)
    return mfccs
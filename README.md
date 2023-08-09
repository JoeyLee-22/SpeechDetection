# Speech Detection Model
## SVM Classifier used to predict how much speech is detected in a wav file

- - -

### Config file for the SVM

`model_filename`:name of file to save model to or load model from

`audio_filename`:path to audio file to predict

`demo_mode`:T/F

`predict`:T/F

`train_model`:T/F

`load_model`:T/F

`save_model`:T/F

`n_mfcc`:number of mfcc to compute

`n_fft`:number of samples in each fourier transform

`hop_length`:number of samples between successive frames

- - - 

### mfModel.py

Uses config file to determine what needs to be done.

When `demo_mode` is true it will only create the demo graph

Otherwise the code will either create a new SVM classifer or load an old one and make a prediction


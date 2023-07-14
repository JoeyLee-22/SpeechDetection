import os
import azure.cognitiveservices.speech as speechsdk

def get_text(audio_config):
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    speech_config.speech_recognition_language="en-US"

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return("{}".format(speech_recognition_result.text))
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        return("")
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        return("Speech Recognition canceled: {}".format(cancellation_details.reason))
        # if cancellation_details.reason == speechsdk.CancellationReason.Error:
        #     return("Error details: {}".format(cancellation_details.error_details))
        #     return("Did you set the speech resource key and region values?")

# directory = "audio"
# for filename in os.listdir(directory):
#     f = os.path.join(directory, filename)
#     if os.path.isfile(f):
#         print("\nAUDIO FILE: {}".format(f))
#         recognize_from_file(speechsdk.audio.AudioConfig(filename=f))
# print("\n")
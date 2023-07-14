import google.cloud.texttospeech as tts
from scipy.io.wavfile import write

def text_to_wav(voice_name: str, text: str, file_name: str):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config,
    )

    filename = f"audio/{file_name}.wav"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Generated speech saved to "{filename}"')
        
# text_to_wav("en-US-Studio-O", "A", "s1")
# text_to_wav("en-US-Studio-O", "E", "s2")
# text_to_wav("en-US-Studio-O", "I", "s3")
# text_to_wav("en-US-Studio-O", "O", "s4")
# text_to_wav("en-US-Studio-O", "U", "s5")
# text_to_wav("en-US-Studio-O", "A, E, I, O, U, A, E, I, O, U.", "s5")
# text_to_wav("en-US-Wavenet-A", "Siri became confused when we reused to follow her directions.", "s2")
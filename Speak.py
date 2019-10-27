from os import environ, remove
from os.path import exists
environ["GOOGLE_APPLICATION_CREDENTIALS"] = "YHH.json"


def cleanup(file_name):
    if exists(file_name):
        remove(file_name)
    return None


def synthesize_text(text, output='NewFile.bin', effects_profile_id='handset-class-device'):
    """ Specifically for mobile and handset devices! """
    from google.cloud import texttospeech as tts

    client = tts.TextToSpeechClient()
    input_text = tts.types.SynthesisInput(text=text)
    voice = tts.types.VoiceSelectionParams(language_code='en-US')

    audio_config = tts.types.AudioConfig(
        audio_encoding=tts.enums.AudioEncoding.MP3,
        effects_profile_id=[effects_profile_id])

    response = client.synthesize_speech(input_text, voice, audio_config)

    # The response's audio_content is some strange binary format
    with open(output, 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file "{}"'.format(output))


def speak(audio_file):
    pass

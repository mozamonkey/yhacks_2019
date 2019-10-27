"""
Y-HACKS 2019

ISHAN MISHRA
MATHEW MOZAFFARI
"""

from os import environ
from Transcribe import main as transcribe
from Speak import synthesize_text


# Run authentication
environ["GOOGLE_APPLICATION_CREDENTIALS"] = "YHH.json"


def voice_input():
    """ User's voice input ---> Text """
    transcribe()  # this prints out the transcribed text
    return None


def speak(text, output_file):
    """ Read text out loud! """
    synthesize_text(text, output_file, effects_profile_id='handset-class-device')
    return None


if __name__ == '__main__':
    print('Transcribing your text now: ')
    voice_input()

    print('Saving a poem to memory now!')
    speak("It matters not how straight the gate. "
          "Or how charged with punishments, the scroll. "
          "I am the master of my fate. "
          "I am the captain of my soul.", "Invictus.mp3")

""" Y-HACKS 2019
ISHAN MISHRA
MATHEW MOZAFFARI"""

from numpy import array
import pyttsx3
import speech_recognition as sr

import googlemaps
from datetime import datetime

# Define dictionary constant
mapping = {
    ' ': ' ',

    'A': array([[1, 0],
                [0, 0],
                [0, 0]]),

    'B': array([[1, 0],
                [1, 0],
                [0, 0]]),

    'C': array([[1, 1],
                [0, 0],
                [0, 0]]),

    'D': array([[1, 1],
                [0, 1],
                [0, 0]]),

    'E': array([[1, 0],
                [0, 1],
                [0, 0]]),

    'F': array([[1, 1],
                [1, 0],
                [0, 0]]),

    'G': array([[1, 1],
                [1, 1],
                [0, 0]]),

    'H': array([[1, 0],
                [1, 1],
                [0, 0]]),

    'I': array([[0, 1],
                [1, 0],
                [0, 0]]),

    'J': array([[0, 1],
                [1, 1],
                [0, 0]]),

    'K': array([[1, 0],
                [0, 0],
                [1, 0]]),

    'L': array([[1, 0],
                [1, 0],
                [1, 0]]),

    'M': array([[1, 1],
                [0, 0],
                [1, 0]]),

    'N': array([[1, 1],
                [0, 1],
                [1, 0]]),

    'O': array([[1, 0],
                [0, 1],
                [1, 0]]),

    'P': array([[1, 1],
                [1, 0],
                [1, 0]]),

    'Q': array([[1, 1],
                [1, 1],
                [1, 0]]),

    'R': array([[1, 0],
                [1, 1],
                [1, 0]]),

    'S': array([[0, 1],
                [1, 0],
                [1, 0]]),

    'T': array([[0, 1],
                [1, 1],
                [1, 0]]),

    'U': array([[1, 0],
                [0, 0],
                [1, 1]]),

    'V': array([[1, 0],
                [1, 0],
                [1, 1]]),

    'W': array([[0, 1],
                [1, 1],
                [0, 1]]),

    'X': array([[1, 1],
                [0, 0],
                [1, 1]]),

    'Y': array([[1, 1],
                [0, 1],
                [1, 1]]),

    'Z': array([[1, 0],
                [0, 1],
                [1, 1]]),
}


# Define response variables
response = {
    "sucess" : True,
    "failure": False,
    "transcription": None
}


def get_key():
    with open('GoogleMaps.txt', 'r') as f:
        for line in f:
            key = line.strip()
    return key


def voice_input():
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        response["transcription"] = r.recognize_google(audio)
    except sr.RequestError:
        response["sucess"] = False
        response["error"] = "API Unavilable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"
    return response


def get_braille(text: str):
    return [mapping[char.upper()] for char in text]


def vibrate(braille_sequence):
    """ Need to figure out how to map Braille sequences to Vibration patterns """
    pass


def speak(text: str, engine_handle):
    engine_handle.say(text)
    pass


def tutorial():
    pass


def startup():
    new_engine = pyttsx3.init()
    new_engine.say("Welcome to Braillient!")
    new_engine.say("Here's a quick tutorial!")
    tutorial()
    return new_engine


def ask_maps(engine_handle, client_handle):
    location = voice_input()["transcription"]

    now = datetime.now()
    directions = gmaps.directions(location, mode="walking",
                                         departure_time=now)
    return directions


if __name__ == '__main__':

    # Initialize everything
    r = sr.Recognizer()
    engine = startup()
    mic = sr.Microphone()
    gmaps = googlemaps.Client(key=get_key())

    tutorial()

    engine.say("Where would you like to go?")
    resp = voice_input()
    if resp["transcription"]:
        instructions = ask_maps(engine, gmaps)

    pass

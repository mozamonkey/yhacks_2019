from __future__ import division

from os import environ

import re
import sys

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue
from time import time

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

# Authentication
environ["GOOGLE_APPLICATION_CREDENTIALS"] = "YHH.json"


class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)


def parse_words(responses, initial_time):
    counter = 0  # number of characters that have been printed
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript  # Top alternative
        overwrite = ' ' * (counter - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite + '\r')
            sys.stdout.flush()

            counter = len(transcript)

        else:
            print(transcript + overwrite)

            # Exit condition
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..')
                break
            elif time()-initial_time > 60:
                print('Timeout!')
                break
            elif counter > 40:
                print('Big address!')
                break

            counter = 0


def main():
    language_code = 'en-US'

    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)
        parse_words(responses, time())


if __name__ == '__main__':
    main()

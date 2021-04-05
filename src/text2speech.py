# -*- coding: utf-8 -*-
"""
Text to speech using Azure API
https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-text-to-speech?tabs=script%2Cwindowsinstall&pivots=programming-language-python
""" 
import base64
import requests

# Creates a speech synthesizer using the default speaker as audio output.
# speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

_voice_list = [("en-US-Wavenet-A", "English, United States (en-US-Wavenet-A)")]

def options():
    """
    Provides access to voice only.
    """
    return [
        dict(
            key='voice',
            label="Voice",
            values=_voice_list,
            transform=lambda value: value,
            default='en-US-Wavenet-D',
        ),

        dict(
            key='speed',
            label="Speed",
            values=(0.25, 4),
            transform=float,
            default=1.00,
        ),

        dict(
            key='pitch',
            label="Pitch",
            values=(-20.00, 20.00),
            transform=float,
            default=0.00,
        ),
        dict(
            key='profile',
            label="Profile",
            values=[("default", "Default")],
            transform=lambda value: value,
            default='default',
        )
    ]

def run(text, options, path):
    """
    Send a synthesis request to the Text-to-Speech API and
    decode the base64-encoded string into an audio file.
    """
    payload = {
        "audioConfig": {
            "audioEncoding": "MP3",
        },
        "input": {
            "text":"Android is a mobile operating system developed by Google, based on the Linux kernel and designed primarily for touchscreen mobile devices such as smartphones and tablets"
        },
        "voice": {
            "languageCode": 'en-gb',
            "name": "en-GB-Standard-A"
        }
    }

    headers = {
        'x-origin': 'https://explorer.apis.google.com'
    }

    # if options['profile'] != 'default':
        # payload["audioConfig"]["effectsProfileId"] = [options['profile']]

    # r = requests.post("https://texttospeech.googleapis.com/v1/text:synthesize?key=AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM", headers=headers, json=payload)
    r = requests.post("https://texttospeech.googleapis.com/v1/text:synthesize?key=AIzaSyCwFLG0eG225i0yV-OxSEKODkw4pih_DAI", headers=headers, json=payload)

    r.raise_for_status()

    data = r.json()
    print("data is: ")
    print(data)
    encoded = data['audioContent']
    audio_content = base64.b64decode(encoded)

    with open(path, 'wb') as response_output:
        print("writing speech to path: "+ path)
        response_output.write(audio_content)

def text2speech(input_text):
    # Receives a text from console input.
    print("Type some text that you want to speak...")
    text = "How are you doing? Type some text that you want to speak..."

    run(text, options(), "/Users/kabhishek/Documents/fsdl-talk-to-transformer/test.mp3")

    # curl 'https://translate.google.com/translate_tts?ie=UTF-8&q=Hello%20Everyone&tl=en&client=tw-ob' -H 'Referer: http://translate.google.com/' -H 'User-Agent: stagefright/1.2 (Linux;Android 5.0)' > google_tts.mp3

    # import requests
    # url = 'https://translate.google.com/translate_tts?ie=UTF-8&q={}&tl=en&client=tw-ob'.format(text)
    # # payload = open("request.json")
    # headers = {"User-Agent": "stagefright/1.2 (Linux;Android 5.0)", "Referer": "http://translate.google.com/"}
    # r = requests.post(url, headers=headers)
    # r.text

    # Synthesizes the received text to speech.
    # The synthesized speech is expected to be heard on the speaker with this line executed.
    # speech_synthesizer.speak_text_async(text).get()

    # audio_config = AudioOutputConfig(use_default_speaker=True)


    # for writing to a file
    # audio_config = AudioOutputConfig(filename="path/to/write/file.wav")
    # synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    # synthesizer.speak_text_async("A simple test to write to a file.")

    # audio_config = AudioOutputConfig(use_default_speaker=True)

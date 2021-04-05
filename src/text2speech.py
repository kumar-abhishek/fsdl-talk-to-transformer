# -*- coding: utf-8 -*-
"""
Text to speech using Azure API
https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-text-to-speech?tabs=script%2Cwindowsinstall&pivots=programming-language-python
""" 
import base64
import requests
import streamlit as st

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
            "text": text
        },
        "voice": {
            "languageCode": 'en-gb',
            "name": "en-GB-Standard-A"
        }
    }
    headers = {
        'x-origin': 'https://explorer.apis.google.com'
    }
    r = requests.post("https://texttospeech.googleapis.com/v1/text:synthesize?key=AIzaSyCwFLG0eG225i0yV-OxSEKODkw4pih_DAI", headers=headers, json=payload)
    r.raise_for_status()
    data = r.json()
    encoded = data['audioContent']
    audio_content = base64.b64decode(encoded)

    with open(path, 'wb') as response_output:
        print("writing speech to path: "+ path)
        response_output.write(audio_content)

def text2speech(input_text):
    # Receives a text from console input.
    print("Type some text that you want to speak...")
    text = "How are you doing? Type some text that you want to speak..."

    run(text, options(), "test.mp3")

    if st.button('Play generated text'):
        try:
            audio_file = open("test.mp3", 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/wav')
        except:
            st.write("Please record sound first")
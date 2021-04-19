# -*- coding: utf-8 -*-
import streamlit as st
import torch
import IPython

WAVE_OUTPUT_FILE = '/tmp/test.wav'

"""
Using coqui-ai/TTS: https://github.com/coqui-ai/TTS
Sample code: https://colab.research.google.com/drive/1iAe7ZdxjUIuN6V4ooaCt0fACEGKEn7HW?usp=sharing#scrollTo=FuHUxvHDf8sX
"""
def text2speech(input_text):
    synthesizer = torch.hub.load('coqui-ai/TTS:dev', 
                                'tts', 
                                source='github')
    wav = synthesizer.tts(input_text)
    audio_obj = IPython.display.Audio(wav, rate=synthesizer.ap.sample_rate)
    with open(WAVE_OUTPUT_FILE, 'wb') as f:
        f.write(audio_obj.data)

    with open(WAVE_OUTPUT_FILE, 'rb') as audio_file:
        st.audio(audio_file, format='audio/wav')
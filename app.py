import time, os
import logging
import streamlit as st
import numpy as np
import librosa, librosa.display
import matplotlib.pyplot as plt
import SessionState
from PIL import Image
from settings import IMAGE_DIR, DURATION, WAVE_OUTPUT_FILE
from src.sound import sound
from src.model import CNN
from setup_logging import setup_logging
from src.speech2text import speech2text
from src.generate_text import generate_text
from src.text2speech import text2speech
from streamlit import caching

setup_logging()
logger = logging.getLogger('app')

def init_model():
    cnn = CNN((128, 87))
    cnn.load_model()
    return cnn

def get_spectrogram(type='mel'):
    logger.info("Extracting spectrogram")
    y, sr = librosa.load(WAVE_OUTPUT_FILE, duration=DURATION)
    ps = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    logger.info("Spectrogram Extracted")
    format = '%+2.0f'
    if type == 'DB':
        ps = librosa.power_to_db(ps, ref=np.max)
        format = ''.join[format, 'DB']
        logger.info("Converted to DB scale")
    return ps, format

def display(spectrogram, format):
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(spectrogram, y_axis='mel', x_axis='time')
    plt.title('Mel-frequency spectrogram')
    plt.colorbar(format=format)
    plt.tight_layout()
    st.pyplot(clear_figure=False)

def main():
    col1, mid, col2 = st.beta_columns([10,1,10])
    with col1:
        image = Image.open(os.path.join(IMAGE_DIR, 'speak.jpg'))
        st.image(image, width=200)
    with col2:
        image = Image.open(os.path.join(IMAGE_DIR, 'unicorn.jpg'))
        st.image(image, width=200)

    title = "Talk to Transformer"
    st.title(title)

    session_state = SessionState.get(name="", button_sent=False)
    record_button_clicked = st.button('Record')
    if record_button_clicked or session_state.button_sent: # <-- first time is button interaction, next time use state:
        st.empty()
        session_state.button_sent = True
        if record_button_clicked:
            # you can get some voice samples from here: https://huggingface.co/facebook/wav2vec2-base-960h
            with st.spinner(f'Recording for {DURATION} seconds ....'):
                sound.record()
            st.success("Recording completed")

            if st.button('Play'):
                try:
                    audio_file = open(WAVE_OUTPUT_FILE, 'rb')
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format='audio/wav')
                except:
                    st.write("Please record sound first")

        st.subheader("Here is what you spoke:\n")
        if record_button_clicked:
            session_state.input_text = speech2text(WAVE_OUTPUT_FILE)
            session_state.input_text = session_state.input_text.capitalize()
            for question_str in ['Which ', 'Why ', 'Who ', 'Whose ', 'Whom ', 'What ', 'How ']: 
                if session_state.input_text.startswith(question_str):
                    session_state.input_text += '?'
                    break
        st.write(session_state.input_text)
        
        st.subheader("Generating text using Transformer(DistilGPT2) model: \n")
        if record_button_clicked:
            session_state.gen_txt = generate_text(session_state.input_text)
        st.write(session_state.gen_txt)

        with st.spinner('Converting text to speech...'):
            text2speech(session_state.gen_txt)

if __name__ == '__main__':
    main()

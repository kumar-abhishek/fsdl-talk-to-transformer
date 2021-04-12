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

        st.write("Here is what you spoke:\n")
        if record_button_clicked:
            session_state.input_text = speech2text(WAVE_OUTPUT_FILE)
        st.write(session_state.input_text)
        
        st.write("Generating text using Transformer model: \n")
        if record_button_clicked:
            session_state.gen_txt = generate_text(session_state.input_text)
        st.write(session_state.gen_txt)

        text2speech(session_state.gen_txt)

    # if st.button('Classify'):
    #     cnn = init_model()
    #     with st.spinner("Classifying the chord"):
    #         chord = cnn.predict(WAVE_OUTPUT_FILE, False)
    #     st.success("Classification completed")
    #     st.write("### The recorded chord is **", chord + "**")
    #     if chord == 'N/A':
    #         st.write("Please record sound first")
    #     st.write("\n")

    # # Add a placeholder
    # if st.button('Display Spectrogram'):
    #     # type = st.radio("Scale of spectrogram:",
    #     #                 ('mel', 'DB'))
    #     if os.path.exists(WAVE_OUTPUT_FILE):
    #         spectrogram, format = get_spectrogram(type='mel')
    #         display(spectrogram, format)
    #     else:
    #         st.write("Please record sound first")

if __name__ == '__main__':
    main()
    # for i in range(100):
    #   # Update the progress bar with each iteration.
    #   latest_iteration.text(f'Iteration {i+1}')
    #   bar.progress(i + 1)
    #   time.sleep(0.1)


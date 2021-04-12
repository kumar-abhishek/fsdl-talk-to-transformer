# -*- coding: utf-8 -*-
"""Speech Transcript with Hugging Face 🤗 Transformers.ipynb

Original file is located at
    https://colab.research.google.com/gist/kumar-abhishek/80a8f9a53974b1daaabf79f903f31317/speech-transcript-with-hugging-face-transformers.ipynb
"""

import librosa
import os
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

# to disable TOKENIZERS_PARALLELISM=(true | false) warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

#load pre-trained model and tokenizer
tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")


def speech2text(wavFileFullPath):
    #load any audio file of your choice
    speech, rate = librosa.load(wavFileFullPath,sr=16000)

    import IPython.display as display
    display.Audio(wavFileFullPath)

    input_values = tokenizer(speech, return_tensors = 'pt').input_values

    #Store logits (non-normalized predictions)
    logits = model(input_values).logits

    logits

    #Store predicted id's
    predicted_ids = torch.argmax(logits, dim =-1)

    #decode the audio to generate text
    transcriptions = tokenizer.decode(predicted_ids[0])
    print(transcriptions)
    return transcriptions


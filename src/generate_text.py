# -*- coding: utf-8 -*-
"""
Text generation using transformer model
Reference: https://www.kaggle.com/tuckerarrants/text-generation-with-huggingface-gpt2#II.-Different-Decoding-Methods
""" 

#get deep learning basics
from transformers import pipeline, set_seed


#for reproducability
SEED = 34
#maximum number of words in output text
MAX_LEN = 150

def generate_text(start_text):
    generator = pipeline('text-generation', model='gpt2')
    set_seed(42)
    return generator(start_text, max_length=MAX_LEN, num_return_sequences=1)
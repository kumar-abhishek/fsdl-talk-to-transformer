# -*- coding: utf-8 -*-
"""
Text generation using transformer model
Reference: https://www.kaggle.com/tuckerarrants/text-generation-with-huggingface-gpt2#II.-Different-Decoding-Methods
""" 

# #get deep learning basics
# import tensorflow as tf
# from transformers import TFGPT2LMHeadModel, GPT2Tokenizer
# from transformers import pipeline, set_seed


# #for reproducability
# SEED = 34
# #maximum number of words in output text
# MAX_LEN = 150

# def generate_text(start_text):
#     generator = pipeline('text-generation', model='gpt2')
#     set_seed(42)
#     return generator(start_text, max_length=MAX_LEN, num_return_sequences=1)

# def generate_text(start_text):
#     generator = pipeline('text-generation', model='distilgpt2')
#     set_seed(42)
#     return generator(start_text, max_length=MAX_LEN, num_return_sequences=1)    

# https://github.com/marcalph/textnets/blob/4327a86b56ecf346bd43619ee0f0e0285563c338/src/compose/baseline.py
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
torch.manual_seed(42)
tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")
model = GPT2LMHeadModel.from_pretrained("distilgpt2", pad_token_id=tokenizer.eos_token_id)


def generate_text(string, possibilities=1):
    """ composition func
    Parameters
    ----------
    string : starting string
    Returns
    -------
    output : completed string
    """
    input = tokenizer.encode(string, return_tensors='pt')
    sampling_outputs = model.generate(
        input,
        do_sample=True,
        max_length=50,
        top_k=50,
        top_p=0.95,
        num_return_sequences=possibilities)
    txt = [tokenizer.decode(sample, skip_special_tokens=True) for sample in sampling_outputs][0]
    return txt[:txt.rfind('.')+1]
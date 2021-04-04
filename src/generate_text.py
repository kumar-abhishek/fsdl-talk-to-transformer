# -*- coding: utf-8 -*-
"""
Text generation using transformer model
Reference: https://www.kaggle.com/tuckerarrants/text-generation-with-huggingface-gpt2#II.-Different-Decoding-Methods
""" 

#get deep learning basics
import tensorflow as tf
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer

#for reproducability
SEED = 34
#maximum number of words in output text
MAX_LEN = 150

# tf.random.set_seed(SEED)


def generate_text(start_text):
    #get large GPT2 tokenizer and GPT2 model
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2-large")
    GPT2 = TFGPT2LMHeadModel.from_pretrained("gpt2-large", pad_token_id=tokenizer.eos_token_id)

    prompt3 = 'Legolas and Gimli advanced on the orcs, raising their weapons with a harrowing war cry.'
    input_ids = tokenizer.encode(prompt3, return_tensors='tf')

    sample_outputs = GPT2.generate(
                                input_ids,
                                do_sample = True, 
                                max_length = MAX_LEN, #to test how long we can generate and it be coherent
                                #temperature = .8,
                                top_k = 50, 
                                top_p = 0.85 
                                #num_return_sequences = 5
    )

    print("Output:\n" + 100 * '-')
    for i, sample_output in enumerate(sample_outputs):
        return(tokenizer.decode(sample_output, skip_special_tokens = True))
        #print("{}: {}...".format(i, tokenizer.decode(sample_output, skip_special_tokens = True)))
        # print('')
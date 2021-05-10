# -*- coding: utf-8 -*-
"""
Text generation using transformer model
Reference: https://www.kaggle.com/tuckerarrants/text-generation-with-huggingface-gpt2#II.-Different-Decoding-Methods
# https://github.com/marcalph/textnets/blob/4327a86b56ecf346bd43619ee0f0e0285563c338/src/compose/baseline.py
"""
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
        max_length=100,
        top_k=50,
        top_p=0.95,
        num_return_sequences=3)
    all_predictions = [tokenizer.decode(sample, skip_special_tokens=True) for sample in sampling_outputs]
    print("all_predictions: ")
    print(all_predictions)
    final_prediction = None
    # remove bad predictions:
    for prediction in all_predictions:
        if prediction is None or '' or prediction.endswith('\n\n\n\n\n') or prediction.count('.')>5:
            continue
        else:
            if '.' in prediction: # remove incomplete sentence in the end
                 prediction = prediction[:prediction.rfind('.')+1]
            final_prediction = prediction
            break

    print('\nbefore: final_prediction:' + final_prediction)

    # add some dummy prediction            
    if not final_prediction:
        final_prediction = "Sorry, I can't relate to what you said really!"
    else:
        print('\nfinal_prediction:' + final_prediction)
    return final_prediction
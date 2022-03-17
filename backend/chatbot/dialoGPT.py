from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")


def get_reply(message, step, chat_history_ids=None, max_len=1000):
    # encode message
    new_user_input_ids = tokenizer.encode(message + tokenizer.eos_token, return_tensors='pt')
    
    # append the new user input tokens to the chat history
    bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

    # generate response
    chat_history_ids = model.generate(chat_history_ids, max_length=max_len, pad_token_id=tokenizer.eos_token_id)

    # get string
    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    return response, chat_history_ids

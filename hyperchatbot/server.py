import uvicorn
from fastapi import FastAPI
import logging

import random
import torch
from nltk_utils import bag_of_words, tokenize

from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = None
model = None


def do_startup():
    global tokenizer, model
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")


def get_reply(message, step, chat_history_ids=None, max_len=10000):
    global tokenizer, model
    # encode message
    new_user_input_ids = tokenizer.encode(
        message + tokenizer.eos_token, return_tensors='pt')

    # append the new user input tokens to the chat history
    bot_input_ids = torch.cat(
        [chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

    # generate response
    chat_history_ids = model.generate(
        bot_input_ids, max_length=max_len, pad_token_id=tokenizer.eos_token_id)

    # get string
    response = tokenizer.decode(
        chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    return response, chat_history_ids


app = FastAPI()
logger = logging.getLogger("gunicorn.error")

all_words = None
tags = None
intents, bot_name, model, device = None, None, None, None


class ChatbotState:
    step: int = 0
    chat_history_ids = None


chatbot_state = ChatbotState()


@app.on_event("startup")
async def startup_event():
    do_startup()


@app.get("/")
def get_root():
    return {"AGVN": "ChatbotTM"}


def check_reset():
    '''
    Reset the model if required.
    '''
    global chatbot_state
    if chatbot_state.step > 4:
        chatbot_state.step = 0
        chatbot_state.chat_history_ids = None


@app.get("/message/")
def send_message(message: str):
    # Call NLTK chatbot API, wait for response -> can be problematic
    response = handle_chat(message)
    check_reset()
    return {"message": response}


def handle_chat(message):
    global chatbot_state
    data = get_reply(message, chatbot_state.step,
                     chatbot_state.chat_history_ids)
    logger.info("data:", data)
    response, chat_history_ids = data[0], data[1]
    logger.info("response:", response)
    logger.info("chat_history_ids:", chat_history_ids)
    chatbot_state.step += 1
    chatbot_state.chat_history_ids = chat_history_ids
    return response


def call_chatbot(input):
    global all_words, tags, intents, bot_name, model, device

    sentence = tokenize(input)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                # output upon understanding
                response = random.choice(intent['responses'])
    else:
        # output upon not understanding
        response = f"{bot_name}: I do not understand..."

    return response


def run_server():
    uvicorn.run(app, host="0.0.0.0", port=1337)


if __name__ == "__main__":
    run_server()

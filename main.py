from fastapi import FastAPI, Request
from pydantic import BaseModel
import httpx
import os
import openai
import constants as constants

TOKEN = "5764835537:AAEVeCtTnGPtfsupAh-mJF08ajoYJY6EI2I"
BASE_URL_TELEGRAM = f"https://api.telegram.org/bot{TOKEN}"
BASE_URL_SLACK = "https://hooks.slack.com/services/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"
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = httpx.AsyncClient()

# CUSTOM MESSAGES
def get_chatgpt_response(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages)

    return response['choices'][0]['message']['content']

def get_initial_message():
    messages=[{"role": "system", "content": constants.INIT_CHATBOT_PROMPT}]
    return messages

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

app = FastAPI()

@app.get("/")
async def root():

    return {"message": "Hello World. Welcome to FastAPI!"}

@app.post("/telegram")
async def webhook(req: Request):

    data = await req.json()
    chat_id = data['message']['chat']['id']
    text = data['message']['text']
    response = "SOMETHING WENT WRONG"

    if text == "/start":
        messages = get_initial_message()
        response = get_chatgpt_response(messages)
    else:
        response = get_chatgpt_response([{"role": "user", "content": text}])

    await client.get(f"{BASE_URL_TELEGRAM}/sendMessage?chat_id={chat_id}&text={response}")

    return data

@app.post("/slack")
async def webhook(req: Request):

    # TODO: chiamate a OPENAI

    return "yolo"


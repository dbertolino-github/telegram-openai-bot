from fastapi import FastAPI, Request
from pydantic import BaseModel
import httpx
import os
import openai
import constants as constants
from pydantic import BaseModel
from postgres_client import PostgreSQLClient
import urllib
from unidecode import unidecode

TOKEN = os.environ["TELEGRAM_TOKEN"]
BASE_URL_TELEGRAM = f"https://api.telegram.org/bot{TOKEN}"
BASE_URL_SLACK = os.environ["BASE_URL_SLACK"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = httpx.AsyncClient()

class SlackMessage(BaseModel):
    text: str

# CUSTOM MESSAGES
def get_chatgpt_response(messages, model="gpt-3.5-turbo"):
    try :
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=200)
    except :
        print("ERRORE OPENAI")

    return response['choices'][0]['message']['content']

def get_initial_message(chat_id, name):
    message = constants.INIT_CHATBOT_PROMPT.format(name)
    messages=[{"role": "system", "content": message}]
    db_client.insert_message(chat_id, "system", message)
    print(message)
    return messages

def manage_incoming_message(chat_id, text, name):

    response = "SOMETHING_WENT_WRONG"
    if text == "/start":
        messages = get_initial_message(chat_id, name)
        response = get_chatgpt_response(messages)
        db_client.insert_message(chat_id, "system", response)
    else:
        response = get_chatgpt_response([{"role": "user", "content": text}])
    
    db_client.insert_message(chat_id, "user", text)
    db_client.insert_message(chat_id, "assistant", response)

    return response

# build a table mapping all non-printable characters to None
NOPRINT_TRANS_TABLE = {
    i: None for i in range(0, sys.maxunicode + 1) if not chr(i).isprintable()
}

def make_printable(s):
    """Replace non-printable characters in a string."""

    # the translate method on str removes characters
    # that map to None from the string
    return s.translate(NOPRINT_TRANS_TABLE)

db_client = PostgreSQLClient()
app = FastAPI()

@app.get("/")
async def root():

    return {"message": "Hello World. Welcome to FastAPI!"}

@app.post("/telegram")
async def webhook(req: Request):

    data = await req.json()
    chat_id = data['message']['chat']['id']
    text = data['message']['text']
    name = data['message']['from']['first_name']
    response = manage_incoming_message(chat_id, text, name)
    response = make_printable(response)
    url = f"{BASE_URL_TELEGRAM}/sendMessage?chat_id={chat_id}&text={response}"
    # url = urllib.parse.quote(url.encode('utf8'), ':/')
    await client.get(url)

    return data

@app.post("/slack")
async def webhook(req: SlackMessage):
    print(req)
    response = manage_incoming_message(req.text)
    print(response)

    return response['text']
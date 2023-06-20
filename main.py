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
import sys

TOKEN = os.environ["TELEGRAM_TOKEN"]
BASE_URL_TELEGRAM = f"https://api.telegram.org/bot{TOKEN}"
BASE_URL_SLACK = os.environ["BASE_URL_SLACK"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = httpx.AsyncClient()

class SlackMessage(BaseModel):
    text: str

def from_tuple_to_gpt_input(tuples): 
    list = []
    for t in tuples : 
        obj = {
            "role" : t[3],
            "content" : t[2]
        }
        list.append(obj)
        
    return list

# CUSTOM MESSAGES
def get_chatgpt_response(messages, model="gpt-3.5-turbo"):
    response = None
    try :
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=.5,
            max_tokens=300)
    except :
        print("ERRORE OPENAI")

    return response['choices'][0]['message']['content']

def summarize(conversation, model="text-davinci-003"):
    final_conversation = ' '.join(conversation)
    augmented_prompt = constants.SUMMARY_PROMPT.format(final_conversation)
    summary = None
    try:
        summary = openai.Completion.create(
            model="text-davinci-003",
            prompt=augmented_prompt,
            temperature=.5,
            max_tokens=500,
        )["choices"][0]["text"]
    except:
        print("ERRORE OPENAI")

    return summary

def get_conversation_transcript(conversation, role):
    user_name = ""
    if role == "assistant":
        user_name = "Alf"
    else:
        user_name = "Il dipendente"
    conversation_text = f"{user_name}: {conversation}"
    return conversation_text

def get_initial_message(chat_id, name):
    message = constants.INIT_CHATBOT_PROMPT.format(name)
    messages=[{"role": "system", "content": message}]
    db_client.insert_message(chat_id, "system", message)
    return messages

def manage_incoming_message(chat_id, text, name):

    response = "SOMETHING_WENT_WRONG"
    conversations = None

    if text == "/start":
        messages = get_initial_message(chat_id, name)
        response = get_chatgpt_response(messages)
    else:
        conversations = db_client.get_messages(chat_id)
        messages = from_tuple_to_gpt_input(conversations)
        messages.append({"role": "user", "content": text})
        response = get_chatgpt_response(messages)
        db_client.insert_message(chat_id, "user", text)
    
    db_client.insert_message(chat_id, "assistant", response)
    
    if conversations:
        transcript = "" 
        l = len(conversations) - 3
        
        for idx, conversation in enumerate(conversations):
            if(idx == 0 or idx > l):
                transcript = transcript+get_conversation_transcript(conversation[2], conversation[3])  
        report = summarize(transcript)

        db_client.insert_report(chat_id, report, report[-6:].replace(' ', '').replace('.', ''))

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

    try : 
        data = await req.json()
        chat_id = data['message']['chat']['id']
        text = data['message']['text']
        name = data['message']['from']['first_name']
        response = manage_incoming_message(chat_id, text, name)
        response = make_printable(response)
        url = f"{BASE_URL_TELEGRAM}/sendMessage?chat_id={chat_id}&text={response}"
        # url = urllib.parse.quote(url.encode('utf8'), ':/')
        await client.get(url)
    
    except Exception as e: 
        print(e)
        response = "SERVER ERROR"
        url = f"{BASE_URL_TELEGRAM}/sendMessage?chat_id={chat_id}&text={response}"
        await client.get(url)

    return data

    

@app.post("/slack")
async def webhook(req: SlackMessage):

    return 'not supported'
from fastapi import FastAPI, Request, HTTPException
import httpx
import os
from postgres_sql_client import PostgreSQLClient
import sys
from chatgpt_manager import ChatGptManager

# Retrieve environment variables
TOKEN = os.environ["TELEGRAM_TOKEN"]
BASE_URL_TELEGRAM = f"https://api.telegram.org/bot{TOKEN}"
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
POSTGRES_HOST = os.getenv("POSTGRES_HOST","")
POSTGRES_DB = os.getenv("POSTGRES_DB","")
POSTGRES_TABLE_CONVERSATIONS =  os.getenv("POSTGRES_TABLE_CONVERSATIONS","")
POSTGRES_TABLE_REPORTS = os.getenv("POSTGRES_TABLE_REPORTS","")
POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME","")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD","")
POSTGRES_PORT = os.getenv("POSTGRES_PORT","")
# build a table mapping all non-printable characters to None
NOPRINT_TRANS_TABLE = {
    i: None for i in range(0, sys.maxunicode + 1) if not chr(i).isprintable()
}

# Init clients for external communications
chatgpt_manager = ChatGptManager(OPENAI_API_KEY)
rest_client = httpx.AsyncClient()
db_client = PostgreSQLClient(POSTGRES_HOST,POSTGRES_DB,POSTGRES_USERNAME,POSTGRES_PASSWORD,POSTGRES_PORT,POSTGRES_TABLE_CONVERSATIONS,POSTGRES_TABLE_REPORTS)
app = FastAPI()

# Server Utils Functions
def manage_incoming_message(chat_id, text, name):
    """
    Helper method to manage an incoming message to the server
    
    :text: content of the message
    :text: name of the user who wrote the message
    :return: a response computed using the chatgpt manager
    :rtype: str
    """
    response = "SOMETHING_WENT_WRONG"
    conversations = None

    if text == "/start":
        messages, init_message = chatgpt_manager.generate_initial_message(name)
        db_client.insert_message(chat_id, "system", init_message)
        response = chatgpt_manager.get_chatgpt_response(messages)
    else:
        conversations = db_client.get_messages(chat_id)
        messages = chatgpt_manager.from_tuple_to_gpt_input(conversations, role_index=3, context_index=2)
        messages.append({"role": "user", "content": text})
        response = chatgpt_manager.get_chatgpt_response(messages)
        db_client.insert_message(chat_id, "user", text)
    
    db_client.insert_message(chat_id, "assistant", response.replace("'", ""))

    return response

def generate_conversation_report(chat_id, username, botname):
    """
    Helper method to generate and save on database a summary of coversation
    
    :chat_id: id of the conversation to summarize
    :username: name to give to the user into the summary
    :botname: name to give to the assistant into the summary

    :return: nothing
    :rtype: None
    """
    conversation = db_client.get_messages(chat_id)

    if conversation:
        transcript = chatgpt_manager.get_conversation_transcript(conversation, username, botname, role_index=3, context_index=2, num_messages=5)
        report = chatgpt_manager.summarize(transcript)

        db_client.insert_report(chat_id, report.replace("'", ""), report[-6:].replace(' ', '').replace('.', '').replace(':', ''))

def make_printable(s):
    """
    Replace non-printable characters in a string.
    
    :s: string to make printable

    :return: printable string
    :rtype: str
    """
    """"""
    return s.translate(NOPRINT_TRANS_TABLE)


@app.get("/")
async def root():
    """
    Function for GET on / path of FastAPI server

    :return: message if server is running
    :rtype: dict
    """
    return {"message": "Hi there, your FastAPI server is online!"}

@app.post("/telegram")
async def telegram_webhook(req: Request):
    """
    Function for POST on /telegram path of FastAPI server.
    This receive an message for telegram server, it compute a response using chagpt and produce a response on /sendMessage versus Telegram servers.

    :return: payload of the incoming request
    :rtype: dict
    """
    try : 
        data = await req.json()
        chat_id = data['message']['chat']['id']
        text = data['message']['text']
        name = data['message']['from']['first_name']
        response = manage_incoming_message(chat_id, text, name)
        response = make_printable(response)
        url = f"{BASE_URL_TELEGRAM}/sendMessage?chat_id={chat_id}&text={response}"
        await rest_client.get(url)
    
    except Exception as e: 
        print(e)
        response = "SERVER ERROR"
        url = f"{BASE_URL_TELEGRAM}/sendMessage?chat_id={chat_id}&text={response}"
        await rest_client.get(url)
        raise HTTPException(status_code=500, detail="Unable to manage incoming message from Telegram")

    return data

@app.post("/conversation-report")
async def generate_conversation_report(req: Request):
    """
    Function for POST on /conversation-report path of FastAPI server.
    This receive a chat-id parameter into the http payload, then compute and store a summary of the corresponding conversation into the database.

    :return: payload of the incoming request
    :rtype: dict
    """
    try : 
        data = await req.json()
        chat_id = data['chat-id']
        generate_conversation_report(chat_id, "Assistant", "User")
    
    except Exception as e: 
        print("SERVER ERROR")
        print(e)
        raise HTTPException(status_code=500, detail="Unable to generate report")

    return data
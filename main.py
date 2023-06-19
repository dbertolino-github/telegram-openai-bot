from fastapi import FastAPI, Request
from pydantic import BaseModel
import httpx
import os

TOKEN = "5764835537:AAEVeCtTnGPtfsupAh-mJF08ajoYJY6EI2I"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

client = httpx.AsyncClient()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World. Welcome to FastAPI!"}


@app.post("/webhook/")
async def webhook(req: Request):
    data = await req.json()
    chat_id = data['message']['chat']['id']
    text = data['message']['text']

    # TODO: chiamate a OPENAI

    response = "sti cazzi non ho l'intelligenza artificiosa"

    await client.get(f"{BASE_URL}/sendMessage?chat_id={chat_id}&text={response}")

    return data
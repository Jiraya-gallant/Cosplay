from fastapi import FastAPI
from pyrogram import Client
from bs4 import BeautifulSoup
import requests
import re
import asyncio

app = FastAPI()

api_id = 28607488
api_hash = "bc94e7a874a66b95e28cfbabf8c29948"
channel = "chicas_asiaticas_whaifus_y_mas"

client = Client("telegraph_session", api_id=api_id, api_hash=api_hash)

@app.on_event("startup")
async def startup():
    await client.start()

@app.on_event("shutdown")
async def shutdown():
    await client.stop()

def extract_telegraph_data(url: str):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        title = soup.find('h1').text
        images = [img['src'] if img['src'].startswith('http') else 'https://telegra.ph' + img['src']
                  for img in soup.find_all('img')]
        return {"title": title, "images": images}
    except Exception as e:
        return {"error": str(e)}

@app.get("/latest-albums")
async def get_albums(limit: int = 10):
    messages = []
    async for msg in client.get_chat_history(channel, limit=100):
        if msg.text and "telegra.ph" in msg.text:
            urls = re.findall(r'https?://telegra.ph/[^\s]+', msg.text)
            for url in urls:
                messages.append(url)
                if len(messages) >= limit:
                    break
        if len(messages) >= limit:
            break

    results = []
    for link in messages:
        data = extract_telegraph_data(link)
        results.append({
            "telegraph_url": link,
            **data
        })

    return {"albums": results}

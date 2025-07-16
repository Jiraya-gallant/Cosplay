from fastapi import FastAPI
from pyrogram import Client
from bs4 import BeautifulSoup
import requests
import re

app = FastAPI()

# Your Telegram API credentials
api_id = 28607488
api_hash = "bc94e7a874a66b95e28cfbabf8c29948"

# Channel username (no @)
channel = "chicas_asiaticas_whaifus_y_mas"

# Pyrogram client
client = Client("telegraph_session", api_id=api_id, api_hash=api_hash)

# Start Pyrogram client on FastAPI startup
@app.on_event("startup")
async def startup():
    await client.start()

# Stop Pyrogram client on shutdown
@app.on_event("shutdown")
async def shutdown():
    await client.stop()

# Function to scrape Telegraph title and image URLs
def extract_telegraph_data(url: str):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        title = soup.find('h1').text if soup.find('h1') else "No Title"
        images = [
            img['src'] if img['src'].startswith('http')
            else 'https://telegra.ph' + img['src']
            for img in soup.find_all('img')
        ]
        return {"title": title, "images": images}
    except Exception as e:
        return {"error": str(e)}

# Main endpoint to fetch latest Telegraph posts
@app.get("/latest-albums")
async def get_albums(limit: int = 5):
    found_links = []
    async for msg in client.get_chat_history(channel, limit=100):
        if msg.text and "telegra.ph" in msg.text:
            urls = re.findall(r'https?://telegra.ph/[^\s]+', msg.text)
            for url in urls:
                if url not in found_links:
                    found_links.append(url)
                    if len(found_links) >= limit:
                        break
        if len(found_links) >= limit:
            break

    results = []
    for link in found_links:
        data = extract_telegraph_data(link)
        results.append({
            "telegraph_url": link,
            **data
        })

    return {"albums": results}

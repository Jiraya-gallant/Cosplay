import requests
from bs4 import BeautifulSoup

def extract_telegraph_data(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.title.string.strip() if soup.title else "No Title"
        images = []

        for img in soup.find_all("img"):
            src = img.get("src")
            if src:
                if src.startswith("/file/"):
                    src = f"https://telegra.ph{src}"
                images.append(src)

        return {
            "url": url,
            "title": title,
            "images": images,
            "count": len(images)
        }

    except Exception as e:
        return {"url": url, "error": str(e)}

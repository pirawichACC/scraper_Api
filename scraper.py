import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

url = "https://www.sanook.com/news/laolotto/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

def get_text(keyword):
    tag = soup.find(lambda tag: tag.name in ["h2", "h3"] and keyword in tag.text)
    if tag:
        return tag.find_next().text.strip()
    return ""

data = {
    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "four_digit": get_text("เลขท้าย 4 ตัว"),
    "three_digit": get_text("เลขท้าย 3 ตัว"),
    "two_digit": get_text("เลขท้าย 2 ตัว"),
    "source": url
}

with open("latest.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("updated")
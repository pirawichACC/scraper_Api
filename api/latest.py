from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

def get_lao_lotto():
    url = "https://www.sanook.com/news/laolotto/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # ค้นหา Container ข้อมูล
        item = soup.find('div', class_='lotto-check__res-item')
        date_text = item.find('h2', class_='lotto-check__title').text.strip()
        numbers = [n.text.strip() for n in item.find_all('strong', class_='lotto-check__res-number')]

        return {
            "status": "success",
            "response": {
                "date": date_text,
                "endpoint": "latest",
                "prizes": {
                    "six_digits": numbers[0] if len(numbers) > 0 else "",
                    "five_digits": numbers[1] if len(numbers) > 1 else "",
                    "four_digits": numbers[2] if len(numbers) > 2 else "",
                    "three_digits": numbers[3] if len(numbers) > 3 else "",
                    "two_digits_top": numbers[4] if len(numbers) > 4 else "",
                    "two_digits_bottom": numbers[5] if len(numbers) > 5 else ""
                }
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/latest")
def read_latest():
    return get_lao_lotto()
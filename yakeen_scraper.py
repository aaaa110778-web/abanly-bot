
import requests
from bs4 import BeautifulSoup

def check_sharia(symbol):
    try:
        url = f"https://yaqeen.sa/stocks/{symbol}"
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        tag = soup.find("div", class_="stock-compliance")
        if tag:
            return tag.text.strip()
        return "المعلومة غير متوفرة"
    except:
        return "المعلومة غير متوفرة"

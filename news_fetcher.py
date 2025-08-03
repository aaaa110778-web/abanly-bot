
import requests
from bs4 import BeautifulSoup

def fetch_news(symbol):
    try:
        url = f"https://news.google.com/search?q={symbol}+stock"
        headers = {"User-Agent": "Mozilla/5.0"}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        articles = soup.select("article h3")
        if articles:
            return articles[0].text.strip()
        return "لا توجد أخبار مؤثرة حالياً"
    except:
        return "لا توجد أخبار متوفرة حالياً"


import requests
from bs4 import BeautifulSoup

saudi_links = {
    "الراجحي": "https://www.argaam.com/ar/tadawul/tasi/al-rajhi-bank",
    "سيرا": "https://www.argaam.com/ar/tadawul/tasi/seera-group-holding"
}

def get_saudi_price(name):
    url = saudi_links.get(name)
    if not url:
        return None
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        price_tag = soup.find("td", class_="last")
        return float(price_tag.text.strip()) if price_tag else None
    except:
        return None

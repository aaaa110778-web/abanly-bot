import requests
from bs4 import BeautifulSoup

def get_saudi_price(stock_name):
    try:
        url = f"https://www.argaam.com/ar/disclosures/market-prices/{stock_name}"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        price_tag = soup.find("span", {"class": "market-price"})
        if price_tag:
            return float(price_tag.text.strip())
        return None
    except:
        return None
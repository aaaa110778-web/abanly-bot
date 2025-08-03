symbol_map = {
    "سيرا": "seera",
    "الراجحي": "al-rajhi-bank",
    "أرامكو": "aramco",
    "سابك": "sabic"
}

def get_saudi_price(symbol):
    from bs4 import BeautifulSoup
    import requests

    mapped = symbol_map.get(symbol)
    if not mapped:
        return None

    url = f"https://www.argaam.com/ar/company/{mapped}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    price_tag = soup.find("td", {"id": "last"})
    if price_tag:
        try:
            return float(price_tag.text.strip().replace(",", ""))
        except:
            return None
    return None

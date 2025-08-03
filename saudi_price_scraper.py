
import requests
from bs4 import BeautifulSoup

def get_saudi_price(stock_url_name):
    """
    يحاول جلب السعر اللحظي لسهم سعودي من موقع أرقام.
    
    Args:
        stock_url_name (str): اسم السهم كما يظهر في رابط موقع أرقام (وليس الرمز الرقمي).
            مثال: "الراجحي", "اس تي سي", "دار الأركان"
    
    Returns:
        float | None: السعر إذا تم بنجاح، أو None إذا فشل.
    """
    try:
        url = f"https://www.argaam.com/ar/disclosures/market-prices/{stock_url_name}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        price_tag = soup.find("span", {"class": "market-price"})

        if price_tag:
            price_text = price_tag.text.strip().replace(",", "").replace("٫", ".").split()[0]
            return float(price_text)
        else:
            print("❌ لم يتم العثور على السعر في الصفحة.")
            return None
    except Exception as e:
        print(f"⚠️ خطأ أثناء جلب السعر من أرقام: {e}")
        return None

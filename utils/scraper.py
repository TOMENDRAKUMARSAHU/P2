import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        full_text = soup.get_text(separator="\n")
        # ✅ Limit to 4000 characters to reduce Gemini token load
        return full_text[:4000]
    except Exception as e:
        return f"Error scraping site: {e}"

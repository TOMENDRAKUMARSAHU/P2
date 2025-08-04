
import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        return soup.get_text()
    except Exception as e:
        return f"Error scraping site: {e}"

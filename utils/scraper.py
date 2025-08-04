import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # ✅ Target the first table with movie data
        table = soup.find("table", class_="wikitable")

        if table:
            return table.get_text(separator="\n").strip()

        # Fallback to limited full text if table not found
        full_text = soup.get_text(separator="\n")
        return full_text[:4000]

    except Exception as e:
        return f"Error scraping site: {e}"

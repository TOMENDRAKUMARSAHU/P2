
import requests
from bs4 import BeautifulSoup

def scrape_website(url, max_chars=8000):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        for tag in soup(["script", "style", "footer", "header", "noscript"]):
            tag.decompose()
        parts = []
        for tag in soup.find_all(["h1", "h2", "h3", "p", "li", "table"]):
            txt = tag.get_text(separator=" ", strip=True)
            if txt:
                parts.append(txt)
        return "\n".join(parts)[:max_chars]
    except Exception as e:
        return f"Error scraping site: {e}"

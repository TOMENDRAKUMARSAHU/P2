import requests
from bs4 import BeautifulSoup

def scrape_website(url, max_chars=8000):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "lxml")

        for tag in soup(["script", "style", "header", "footer", "nav", "aside"]):
            tag.decompose()

        content = []
        for tag in soup.find_all(["h1", "h2", "h3", "p", "li", "table"]):
            text = tag.get_text(strip=True)
            if text:
                content.append(text)
            if sum(len(c) for c in content) > max_chars:
                break

        return "\n".join(content)

    except Exception as e:
        return f"Error scraping website: {e}"

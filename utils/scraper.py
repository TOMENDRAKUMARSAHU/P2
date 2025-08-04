import requests
from bs4 import BeautifulSoup

def scrape_website(url, max_chars=8000):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # Remove unnecessary scripts/styles
        for tag in soup(["script", "style", "noscript", "footer", "header", "form", "svg"]):
            tag.decompose()

        # Collect meaningful content: headings, paragraphs, tables
        content_parts = []

        for tag in soup.find_all(["h1", "h2", "h3", "p", "li", "table"]):
            text = tag.get_text(separator=" ", strip=True)
            if text:
                content_parts.append(text)

        # Join parts into one text block
        full_text = "\n".join(content_parts)

        # Limit the length for token budget
        return full_text[:max_chars]

    except Exception as e:
        return f"Error scraping site: {e}"

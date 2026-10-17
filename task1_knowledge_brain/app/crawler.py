
import json
import time
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

import httpx
from bs4 import BeautifulSoup

SITEMAP_URL = (
    "https://support.brilliantdirectories.com/support/sitemap.xml"
)
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
ARTICLES_FILE = DATA_DIR / "articles.json"
ALLOWED_HOST = "support.brilliantdirectories.com"


def get_sitemap_urls() -> list[str]:
    """Read article URLs from the public sitemap."""
    with httpx.Client(timeout=20, follow_redirects=True) as client:
        response = client.get(SITEMAP_URL)
        response.raise_for_status()

    root = ET.fromstring(response.content)
    urls = []

    for element in root.iter():
        if element.tag.endswith("loc") and element.text:
            url = element.text.strip()
            if urlparse(url).hostname == ALLOWED_HOST:
                urls.append(url)

    return list(dict.fromkeys(urls))


def load_saved_articles() -> dict:
    """Load previously downloaded articles so we can resume."""
    if not ARTICLES_FILE.exists():
        return {}

    with ARTICLES_FILE.open("r", encoding="utf-8") as file:
        return {item["url"]: item for item in json.load(file)}


def crawl_articles(limit: int = 10, delay: float = 1.0) -> dict:
    """Download a small batch of articles and save their text and URLs."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    urls = get_sitemap_urls()
    articles = load_saved_articles()
    downloaded = 0
    errors = []

    with httpx.Client(
        timeout=20,
        follow_redirects=True,
        headers={"User-Agent": "AITechConsultantKnowledgeBrain/0.1"},
    ) as client:
        for url in urls:
            if downloaded >= limit:
                break

            if url in articles:
                continue

            try:
                response = client.get(url)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "lxml")
                for element in soup(
                    ["script", "style", "nav", "footer", "header"]
                ):
                    element.decompose()

                title = soup.title.get_text(" ", strip=True) if soup.title else url
                text = soup.get_text(" ", strip=True)

                articles[url] = {
                    "url": url,
                    "title": title,
                    "text": text[:50000],
                }
                downloaded += 1
                time.sleep(delay)

            except (httpx.HTTPError, ValueError) as exc:
                errors.append({"url": url, "error": str(exc)})

    with ARTICLES_FILE.open("w", encoding="utf-8") as file:
        json.dump(list(articles.values()), file, ensure_ascii=False, indent=2)

    return {
        "sitemap_urls_found": len(urls),
        "articles_downloaded_this_run": downloaded,
        "articles_saved_total": len(articles),
        "errors": errors[:10],
    }

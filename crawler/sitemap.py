import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; UniScraper/1.0)"
}


def fetch_sitemap_urls(sitemap_url: str) -> list[str]:
    res = requests.get(sitemap_url, headers=HEADERS, timeout=30)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "xml")
    urls = []

    for loc in soup.find_all("loc"):
        urls.append(loc.text.strip())

    return urls

import os
import time
import requests
from urllib.parse import urlparse

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive",
}


def download_html(url: str, uni_id: str) -> str:
    os.makedirs(f"artifacts/{uni_id}", exist_ok=True)

    #BCAS FIX FORCE TRAILING SLASH
    if not url.endswith("/"):
        url = url + "/"

    filename = urlparse(url).path.strip("/").replace("/", "_") + ".html"
    path = f"artifacts/{uni_id}/{filename}"

    # already downloaded
    if os.path.exists(path):
        return path

    # Add delay before fetching to avoid rate limiting
    time.sleep(1)

    # retry logic
    for attempt in range(3):
        try:
            res = requests.get(url, headers=HEADERS, timeout=30)
            res.raise_for_status()

            with open(path, "w", encoding="utf-8") as f:
                f.write(res.text)

            return path

        except Exception as e:
            if attempt == 2:
                raise e
            time.sleep(3)  # Longer delay before retry


from bs4 import BeautifulSoup
from extractor.base import BaseExtractor

class CINECExtractor(BaseExtractor):

    def extract(self, html, url):
        soup = BeautifulSoup(html, "html.parser")

        def safe(el):
            return el.get_text(strip=True) if el else "Not Available"

        course_name = safe(soup.find("h1"))
        duration = "Not Available"
        eligibility = "Refer course page"

        for li in soup.find_all("li"):
            text = li.get_text(strip=True).lower()
            if "year" in text:
                duration = li.get_text(strip=True)
            if "entry" in text or "eligibility" in text:
                eligibility = li.get_text(strip=True)

        return {
            "course_name": course_name,
            "duration": duration,
            "eligibility_raw": eligibility,
            "source_url": url
        }

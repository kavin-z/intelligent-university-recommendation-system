from bs4 import BeautifulSoup
from extractor.base import BaseExtractor


def safe_text(el):
    return el.get_text(strip=True) if el else None


class BCASExtractor(BaseExtractor):

    def extract(self, html, url):
        soup = BeautifulSoup(html, "html.parser")

        
        course_name = safe_text(soup.find("h1"))

      
        duration = None
        for el in soup.find_all(["p", "li", "span"]):
            t = el.get_text(strip=True).lower()
            if "year" in t or "month" in t:
                duration = el.get_text(strip=True)
                break

      
        eligibility_raw = None
        eligibility_heading = soup.find(
            string=lambda x: x and (
                "entry requirement" in x.lower()
                or "entry qualification" in x.lower()
                or "eligibility" in x.lower()
                or "admission" in x.lower()
            )
        )

        if eligibility_heading:
            parent = eligibility_heading.find_parent(["section", "div"])
            if parent:
                eligibility_raw = parent.get_text(" ", strip=True)

        return {
            "course_name": course_name,
            "duration": duration,
            "eligibility_raw": eligibility_raw,
            "source_url": url
        }

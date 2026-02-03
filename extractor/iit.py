from bs4 import BeautifulSoup
from extractor.base import BaseExtractor


def safe_text(el):
    return el.get_text(strip=True) if el else None


class IITExtractor(BaseExtractor):

    def extract(self, html, url):
        soup = BeautifulSoup(html, "html.parser")

     
        course_name = (
            safe_text(soup.find("h1"))
            or safe_text(soup.select_one("h2"))
        )


        duration = None
        for el in soup.find_all(["p", "li", "span"]):
            text = el.get_text(strip=True).lower()
            if "year" in text or "month" in text:
                duration = el.get_text(strip=True)
                break

       
        eligibility_raw = None
        heading = soup.find(
            string=lambda x: x and (
                "entry requirement" in x.lower()
                or "admission" in x.lower()
            )
        )

        if heading:
            parent = heading.find_parent(["section", "div"])
            if parent:
                eligibility_raw = parent.get_text(" ", strip=True)

        return {
            "course_name": course_name,
            "duration": duration,
            "eligibility_raw": eligibility_raw,
            "source_url": url
        }

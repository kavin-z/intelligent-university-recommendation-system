from bs4 import BeautifulSoup
from extractor.base import BaseExtractor


def safe_text(el):
    return el.get_text(strip=True) if el else None


class SLTCExtractor(BaseExtractor):

    def extract(self, html, url):
        soup = BeautifulSoup(html, "html.parser")

      

        course_name = None

       
        h2 = soup.select_one(
            "div.tab-content-section.section-main h2.elementor-heading-title"
        )
        if h2:
            course_name = safe_text(h2)

       
        if not course_name:
            for el in soup.select("h2.elementor-heading-title"):
                text = safe_text(el)
                if text and "learn." not in text.lower() and "discover" not in text.lower():
                    course_name = text
                    break

        
        if not course_name:
            course_name = (
                url.rstrip("/")
                .split("/")[-1]
                .replace("-", " ")
                .title()
            )



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

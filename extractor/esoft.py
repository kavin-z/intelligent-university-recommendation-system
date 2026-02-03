from bs4 import BeautifulSoup
from extractor.base import BaseExtractor


def safe_text(el):
    return el.get_text(" ", strip=True) if el else None


class ESOFTExtractor(BaseExtractor):

    def extract(self, html, url):
        soup = BeautifulSoup(html, "html.parser")

     
        course_name = None

     
        h1 = soup.select_one("h1")
        if h1:
            course_name = safe_text(h1)

        
        if not course_name:
            h2 = soup.select_one(".elementor-heading-title")
            if h2:
                course_name = safe_text(h2)

        
        if not course_name:
            title = soup.find("title")
            if title:
                course_name = (
                    title.get_text(strip=True)
                    .replace("| ESOFT", "")
                    .replace("ESOFT", "")
                    .strip()
                )

       
        duration = None
        for el in soup.find_all(["p", "li", "span"]):
            text = el.get_text(strip=True).lower()
            if any(k in text for k in ["year", "years", "month", "months"]):
                duration = el.get_text(strip=True)
                break

       
        eligibility_raw = None

        heading = soup.find(
            string=lambda x: x and any(
                k in x.lower()
                for k in [
                    "entry requirement",
                    "eligibility",
                    "admission requirement",
                    "who can apply",
                ]
            )
        )

        if heading:
            container = heading.find_parent(["section", "div"])
            if container:
                eligibility_raw = container.get_text(" ", strip=True)

        return {
            "course_name": course_name,
            "duration": duration,
            "eligibility_raw": eligibility_raw,
            "source_url": url,
        }

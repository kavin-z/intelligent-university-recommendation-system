from bs4 import BeautifulSoup
from extractor.base import BaseExtractor


def safe_text(el):
    return el.get_text(strip=True) if el else None


class NSBMExtractor(BaseExtractor):

    def extract(self, html, url):
        soup = BeautifulSoup(html, "html.parser")

        course_name = safe_text(
            soup.select_one("h2.elementor-heading-title")
        )

        duration = safe_text(
            soup.select_one(".elementor-headline-dynamic-text")
        )

        eligibility_block = soup.find(
            string=lambda x: x and "ENTRY QUALIFICATIONS" in x.upper()
        )

        eligibility_raw = (
            eligibility_block.find_parent("section").get_text(" ", strip=True)
            if eligibility_block else None
        )

        return {
            "course_name": course_name,
            "duration": duration,
            "eligibility_raw": eligibility_raw,
            "source_url": url
        }

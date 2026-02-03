import json

from crawler.discover import discover_course_urls
from downloader.html_downloader import download_html

from extractor.nsbm import NSBMExtractor
from extractor.apiit import APIITExtractor
from extractor.cinec import CINECExtractor
from extractor.kiu import KIUExtractor
from extractor.icbt import ICBTExtractor
from extractor.sltc import SLTCExtractor
from extractor.nibm import NIBMExtractor
from extractor.horizon import HorizonExtractor
from extractor.bcas import BCASExtractor
from extractor.iit import IITExtractor
from extractor.anc import ANCExtractor
from extractor.esoft import ESOFTExtractor
from extractor.sliit import SLIITExtractor

from normalizer.normalize import normalize_course
from db.mongodb import upsert_university, save_course, courses


EXTRACTORS = {
    "nsbm": NSBMExtractor,
    "apiit": APIITExtractor,
    "cinec": CINECExtractor,
    "kiu": KIUExtractor,
    "icbt": ICBTExtractor,
    "sltc": SLTCExtractor,
    "nibm": NIBMExtractor,
    "horizon": HorizonExtractor,
    "bcas": BCASExtractor,
    "iit": IITExtractor,
    "anc": ANCExtractor,
    "esoft": ESOFTExtractor,
    "sliit": SLIITExtractor
}


def university_has_courses(uni_id):
    return courses.count_documents({"university_id": uni_id}) > 0


with open("config/universities.json") as f:
    universities = json.load(f)


for uni in universities:
    print(f"\nProcessing {uni['name']}")

    uni_id = upsert_university(uni)

    #SKIP ALREADY SCRAPED UNIVERSITIES
    if university_has_courses(uni_id):
        print("Already scraped, skipping...")
        continue

    urls = discover_course_urls(uni)
    print(f"Found {len(urls)} course URLs")

    extractor = EXTRACTORS[uni["type"]]()

    for url in urls:
        try:
            html_path = download_html(url, uni["id"])

            with open(html_path, encoding="utf-8") as f:
                html = f.read()

            raw = extractor.extract(html, url)
            normalized = normalize_course(raw)

            save_course(normalized, uni_id)
            print(f"Saved: {normalized['course_name']}")

        except Exception as e:
            print(f"FAILED {url}: {e}")

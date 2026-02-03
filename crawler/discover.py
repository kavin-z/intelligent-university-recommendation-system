import re
import requests
from crawler.sitemap import fetch_sitemap_urls
from crawler.robots import can_fetch



HORIZON_COURSE_REGEX = re.compile(
    r"/(bsc|bm|bit|bed|b_law|msc|med)[a-z0-9_]*$",
    re.IGNORECASE
)



BCAS_EXCLUDE_SLUGS = {
    "business-management",
    "computing",
    "construction-engineering",
    "health-science",
    "hotel-management-tourism",
    "language-education",
    "law",
    "certification",
    "diploma",
    "foundation",
    "higher-national-diploma",
    "bachelors-degree",
    "post-graduate-diploma",
    "master",
    "masters",
    "programme",
}

def is_bcas_course(url: str) -> bool:
    if "/programme/" not in url:
        return False

    slug = url.rstrip("/").split("/")[-1].lower()
    if slug in BCAS_EXCLUDE_SLUGS:
        return False

    return "-" in slug



def is_iit_course(url: str) -> bool:
    return any(p in url for p in [
        "/programme/",
        "/programmes/",
        "/course/",
    ])



def is_anc_course(url: str) -> bool:
    if (
        "/undergraduate-programs/" in url
        or "/postgraduate-programs/" in url
    ):
        slug = url.rstrip("/").split("/")[-1]

        if slug in {
            "undergraduate-programs",
            "postgraduate-programs",
            "uk-undergraduate-programs-top-ups",
            "american-undergraduate-programs",
            "uk-postgraduate-degree-programs",
        }:
            return False

        return "-" in slug

    return False



def is_apiit_course(url: str) -> bool:
    
    if "/courses/" not in url:
        return False
    
    
    exclude_extensions = {'.webp', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.css', '.js', '.pdf'}
    if any(url.lower().endswith(ext) for ext in exclude_extensions):
        return False
    
    return True



def is_sliit_course(url: str) -> bool:

    if "/programmes/" not in url and "/programms/" not in url:
        return False
    
    
    slug = url.rstrip("/").split("/")[-1]
    
    
    if "-" not in slug:
        return False
    
    
    exclude_patterns = ("/blog/", "/news/", "/event", "/about/", "/facilities/", "/staff/", "/contact/")
    if any(pattern in url.lower() for pattern in exclude_patterns):
        return False
    
    return True


def is_esoft_course(url: str) -> bool:
   
    media_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.mp4', '.pdf', '.zip')
    if any(url.lower().endswith(ext) for ext in media_extensions):
        return False
    
    
    if '/wp-content/' in url:
        return False
    
  
    exclude_patterns = (
        "/news/", "/blog", "/event", "/page/",
        "/schools/", "/careers/", "/contact", "/about",
        "/student", "/privacy", "/payment", "/refund", "/quality", "/cookie"
    )
    
    if any(pattern in url.lower() for pattern in exclude_patterns):
        return False
    
   
    slug = url.rstrip("/").split("/")[-1]
    if "-" not in slug:
        return False
    
    return True



def discover_course_urls(university: dict) -> list[str]:

    urls = fetch_sitemap_urls(university["sitemap_url"])
    results = []

    for url in urls:

        if university["type"] == "apiit":
            if not is_apiit_course(url):
                continue

        if university["type"] == "horizon":
            if not HORIZON_COURSE_REGEX.search(url):
                continue

        if university["type"] == "bcas":
            if not is_bcas_course(url):
                continue

        if university["type"] == "iit":
            if not is_iit_course(url):
                continue

        if university["type"] == "anc":
            if not is_anc_course(url):
                continue

        if university["type"] == "sliit":
            if not is_sliit_course(url):
                continue
        
        if university["type"] == "esoft":
            if not is_esoft_course(url):
                continue

        if can_fetch(university["base_url"], url):
            results.append(url)

    return results

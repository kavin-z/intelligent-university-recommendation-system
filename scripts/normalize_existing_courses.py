import sys
import os

# ✅ add project root to PYTHONPATH FIRST
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from pymongo import MongoClient
from services.eligibility_normalizer import normalize_eligibility


client = MongoClient("mongodb://localhost:27017")
db = client["ugc_scraper"]
courses = db["courses"]

for course in courses.find():
    updated = normalize_eligibility(course)

    courses.update_one(
        {"_id": course["_id"]},
        {"$set": {
            "eligibility": updated.get("eligibility"),
            "eligibility_confidence": updated.get("eligibility_confidence"),
            "inferred_from": updated.get("inferred_from")
        }}
    )

print("Eligibility normalization completed.")

from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

#Connection
client = MongoClient("mongodb://localhost:27017")
db = client["ugc_scraper"]

universities = db["universities"]
courses = db["courses"]

#Indexes
universities.create_index("id", unique=True)
courses.create_index("source_url", unique=True)


#Universities
def upsert_university(uni: dict) -> ObjectId:
    """
    Insert or update a university and ALWAYS return its ObjectId.
    """
    result = universities.update_one(
        {"id": uni["id"]},
        {"$set": uni},
        upsert=True
    )

    # If inserted now
    if result.upserted_id:
        return result.upserted_id

    # If already existed
    doc = universities.find_one({"id": uni["id"]})
    if not doc:
        raise RuntimeError("University upsert failed")

    return doc["_id"]


#Courses
def save_course(course: dict, university_id: ObjectId):
    """
    Save a course with a mandatory university_id FK.
    """
    if university_id is None:
        raise ValueError("university_id is None — FK relationship broken")

    course_doc = {
        **course,
        "university_id": university_id,
        "scraped_at": datetime.utcnow()
    }

    courses.update_one(
        {"source_url": course["source_url"]},
        {"$set": course_doc},
        upsert=True
    )

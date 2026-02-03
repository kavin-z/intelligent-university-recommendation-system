from pymongo import MongoClient
import pandas as pd

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["ugc_scraper"]
courses = db["courses"]

# Fetch data
docs = list(courses.find())

# Convert ObjectId to string
for d in docs:
    d["_id"] = str(d["_id"])
    d["university_id"] = str(d.get("university_id"))

# Create DataFrame
df = pd.DataFrame(docs)

# Save to CSV
df.to_csv("courses_raw.csv", index=False)

print(f"Exported {len(df)} courses to courses_raw.csv")

from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
import numpy as np
import os

# Load model (from local path if set, otherwise try to download)
model = None
model_name = os.environ.get("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
local_path = os.environ.get("EMBEDDING_MODEL_PATH")
try:
    if local_path:
        print(f"Loading Sentence-BERT model from local path: {local_path}")
        model = SentenceTransformer(local_path)
    else:
        print(f"Loading Sentence-BERT model: {model_name}")
        model = SentenceTransformer(model_name)  # Fast, lightweight model
    print("AI model loaded successfully!")
except Exception as e:
    print(f"⚠️ Failed to load embedding model ({model_name}): {e}")
    print("If you're offline, set EMBEDDING_MODEL_PATH to a local model directory, or run this script where internet access is available to download the model.")
    raise

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["ugc_scraper"]
courses_col = db["courses"]

print("Generating embeddings for all courses...")
courses = list(courses_col.find())

print(f"Found {len(courses)} courses to process")

for i, course in enumerate(courses):
    # Combine course name and description for better matching
    text = f"{course.get('course_name', '')} {course.get('description', '')} {course.get('keywords', '')}"
    
    # Generate embedding
    embedding = model.encode(text)
    
    # Update course with embedding
    courses_col.update_one(
        {"_id": course["_id"]},
        {"$set": {"embedding": embedding.tolist()}}
    )
    
    if (i + 1) % 100 == 0:
        print(f"Processed {i + 1}/{len(courses)} courses")

print(f"✅ All {len(courses)} course embeddings generated successfully!")

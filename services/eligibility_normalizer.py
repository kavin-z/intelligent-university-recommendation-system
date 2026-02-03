def normalize_eligibility(course: dict) -> dict:
    eligibility = course.get("eligibility", {})
    raw = course.get("eligibility_raw")
    name = (course.get("course_name") or "").lower()

    
    # 1. Explicit eligibility
   
    if eligibility and any(v is not None for v in eligibility.values()):
        course["eligibility_confidence"] = "explicit"
        course["inferred_from"] = []
        return course

  
    # 2. Inference rules
    
    inferred = {}
    inferred_from = []

    # Degree level inference
    if any(k in name for k in ["bsc", "ba", "beng", "bachelor"]):
        inferred["min_al_passes"] = 3
        inferred_from.append("degree_level")

    # Subject inference
    if any(k in name for k in ["engineering", "technology", "it", "software"]):
        inferred["math_required"] = True
        inferred_from.append("course_name")

    if "nursing" in name or "biomedical" in name:
        inferred["biology_required"] = True
        inferred_from.append("course_name")

    if inferred:
        course["eligibility"] = {
            **eligibility,
            **inferred
        }
        course["eligibility_confidence"] = "inferred"
        course["inferred_from"] = inferred_from
        return course

   
    # 3. Unknown
   
    course["eligibility_confidence"] = "unknown"
    course["inferred_from"] = []

    return course

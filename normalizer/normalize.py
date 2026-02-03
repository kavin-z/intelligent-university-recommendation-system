def safe_lower(text):
    return text.lower() if isinstance(text, str) else ""


def normalize_course(raw: dict) -> dict:
    """
    Normalize raw scraped course data.
    MUST NOT handle university_id (DB responsibility).
    """

    eligibility_text = safe_lower(raw.get("eligibility_raw"))
    duration_text = safe_lower(raw.get("duration"))

    return {
        "course_name": raw.get("course_name", "Unknown"),
        "duration": raw.get("duration"),
        "eligibility_raw": raw.get("eligibility_raw"),
        "source_url": raw["source_url"],

        # ML-ready structured fields 
        "eligibility": {
            "requires_al": (
                "a/l" in eligibility_text
                or "advanced level" in eligibility_text
            ),
            "min_al_passes": (
                3 if any(x in eligibility_text for x in ["three", "3 passes"])
                else None
            ),
            "english_required": "english" in eligibility_text,
            "math_required": (
                "math" in eligibility_text
                or "mathematics" in eligibility_text
            )
        }
    }

"""
Advanced AI Features for UniMatch
- Career Path Prediction
- Skill Gap Analysis
- Job Market Alignment
"""

import numpy as np
from typing import Dict, List
from datetime import datetime
import json


# CAREER PATH PREDICTION

CAREER_PATHS = {
    "software-engineering": {
        "progression": [
            {"level": "AL", "field": "Science/Tech", "next": "BSc Software Engineering"},
            {"level": "BSc", "field": "Software Engineering", "next": "MSc Computer Science"},
            {"level": "MSc", "field": "Computer Science", "next": "Senior Developer/Tech Lead"}
        ],
        "careers": [
            {
                "role": "Junior Developer",
                "salary_min": 40000,
                "salary_max": 60000,
                "demand": 95,
                "description": "Entry-level software development role",
                "years_exp": 0,
                "growth": 12
            },
            {
                "role": "Senior Developer",
                "salary_min": 80000,
                "salary_max": 120000,
                "demand": 88,
                "description": "Lead development projects and mentor juniors",
                "years_exp": 3,
                "growth": 8
            },
            {
                "role": "Tech Lead",
                "salary_min": 120000,
                "salary_max": 160000,
                "demand": 75,
                "description": "Architect solutions and manage technical teams",
                "years_exp": 5,
                "growth": 6
            },
            {
                "role": "CTO",
                "salary_min": 150000,
                "salary_max": 250000,
                "demand": 65,
                "description": "Chief Technology Officer, strategic technical leadership",
                "years_exp": 10,
                "growth": 4
            }
        ]
    },
    "data-science": {
        "progression": [
            {"level": "AL", "field": "Science/Maths", "next": "BSc Data Science"},
            {"level": "BSc", "field": "Data Science", "next": "MSc AI/ML"},
            {"level": "MSc", "field": "AI/ML", "next": "Research Scientist/ML Engineer"}
        ],
        "careers": [
            {
                "role": "Data Analyst",
                "salary_min": 45000,
                "salary_max": 65000,
                "demand": 92,
                "description": "Analyze data and create insights",
                "years_exp": 0,
                "growth": 14
            },
            {
                "role": "Data Scientist",
                "salary_min": 75000,
                "salary_max": 110000,
                "demand": 94,
                "description": "Build ML models and predictive analytics",
                "years_exp": 2,
                "growth": 16
            },
            {
                "role": "ML Engineer",
                "salary_min": 100000,
                "salary_max": 150000,
                "demand": 91,
                "description": "Deploy and maintain production ML systems",
                "years_exp": 4,
                "growth": 13
            },
            {
                "role": "AI Research Scientist",
                "salary_min": 130000,
                "salary_max": 200000,
                "demand": 87,
                "description": "Research and develop cutting-edge AI solutions",
                "years_exp": 6,
                "growth": 11
            }
        ]
    },
    "business-management": {
        "progression": [
            {"level": "AL", "field": "Commerce/Science", "next": "BBA/BSc Business"},
            {"level": "BSc", "field": "Business Management", "next": "MBA"},
            {"level": "MBA", "field": "Management", "next": "Executive Director/CEO"}
        ],
        "careers": [
            {
                "role": "Business Analyst",
                "salary_min": 35000,
                "salary_max": 55000,
                "demand": 85,
                "description": "Analyze business processes and drive improvements",
                "years_exp": 0,
                "growth": 7
            },
            {
                "role": "Operations Manager",
                "salary_min": 60000,
                "salary_max": 90000,
                "demand": 80,
                "description": "Manage daily operations and efficiency",
                "years_exp": 2,
                "growth": 6
            },
            {
                "role": "Project Manager",
                "salary_min": 70000,
                "salary_max": 110000,
                "demand": 86,
                "description": "Lead strategic projects and team management",
                "years_exp": 3,
                "growth": 8
            },
            {
                "role": "Director",
                "salary_min": 110000,
                "salary_max": 180000,
                "demand": 72,
                "description": "Executive leadership and strategic planning",
                "years_exp": 8,
                "growth": 5
            }
        ]
    },
    "healthcare": {
        "progression": [
            {"level": "AL", "field": "Science", "next": "BSc Health Sciences"},
            {"level": "BSc", "field": "Healthcare", "next": "MSc Healthcare Management"},
            {"level": "MSc", "field": "Healthcare", "next": "Healthcare Executive"}
        ],
        "careers": [
            {
                "role": "Healthcare Specialist",
                "salary_min": 40000,
                "salary_max": 60000,
                "demand": 88,
                "description": "Provide specialized healthcare services",
                "years_exp": 0,
                "growth": 9
            },
            {
                "role": "Clinical Manager",
                "salary_min": 65000,
                "salary_max": 95000,
                "demand": 82,
                "description": "Manage clinical departments and staff",
                "years_exp": 3,
                "growth": 7
            },
            {
                "role": "Healthcare Administrator",
                "salary_min": 75000,
                "salary_max": 115000,
                "demand": 80,
                "description": "Manage healthcare facility operations",
                "years_exp": 4,
                "growth": 6
            },
            {
                "role": "Medical Director",
                "salary_min": 120000,
                "salary_max": 200000,
                "demand": 75,
                "description": "Lead medical departments and strategy",
                "years_exp": 10,
                "growth": 4
            }
        ]
    }
}


# SKILL REQUIREMENTS BY COURSE

COURSE_SKILLS = {
    "Software Engineering": [
        "Programming (Python, Java, C++)",
        "Web Development",
        "Database Design",
        "System Architecture",
        "Problem Solving",
        "Collaborative Development"
    ],
    "Data Science": [
        "Statistics",
        "Python Programming",
        "Machine Learning",
        "Data Visualization",
        "SQL",
        "Mathematics"
    ],
    "Business Management": [
        "Business Analysis",
        "Leadership",
        "Project Management",
        "Financial Analysis",
        "Communication",
        "Strategic Planning"
    ],
    "Healthcare": [
        "Medical Knowledge",
        "Patient Care",
        "Clinical Skills",
        "Healthcare Systems",
        "Empathy",
        "Attention to Detail"
    ],
    "Engineering": [
        "Mathematics",
        "CAD Software",
        "Physics",
        "Problem Solving",
        "Technical Documentation",
        "Project Management"
    ],
    "Education": [
        "Teaching Methodology",
        "Communication",
        "Subject Expertise",
        "Student Assessment",
        "Classroom Management",
        "Curriculum Development"
    ],
    "Hospitality": [
        "Customer Service",
        "Leadership",
        "Operations Management",
        "Communication",
        "Problem Solving",
        "Cultural Awareness"
    ],
    "Tourism": [
        "Customer Service",
        "Communication",
        "Cultural Knowledge",
        "Organization",
        "Problem Solving",
        "Language Skills"
    ],
    "Psychology": [
        "Research Skills",
        "Analysis",
        "Communication",
        "Empathy",
        "Observation",
        "Critical Thinking"
    ],
    "Civil Engineering": [
        "Mathematics",
        "Physics",
        "CAD Software",
        "Project Management",
        "Technical Documentation",
        "Problem Solving"
    ]
}


# JOB MARKET DATA (Simulated)

JOB_MARKET = {
    "Software Engineering": {"demand": 95, "growth_rate": 12, "trend": "rapidly-growing", "salary_percentile": 85},
    "Data Science": {"demand": 94, "growth_rate": 14, "trend": "rapidly-growing", "salary_percentile": 88},
    "Cybersecurity": {"demand": 91, "growth_rate": 13, "trend": "rapidly-growing", "salary_percentile": 86},
    "Cloud Computing": {"demand": 89, "growth_rate": 11, "trend": "growing", "salary_percentile": 84},
    "Business Management": {"demand": 80, "growth_rate": 6, "trend": "stable", "salary_percentile": 70},
    "Healthcare": {"demand": 88, "growth_rate": 9, "trend": "growing", "salary_percentile": 75},
    "Finance": {"demand": 82, "growth_rate": 5, "trend": "stable", "salary_percentile": 80},
    "Marketing": {"demand": 75, "growth_rate": 4, "trend": "stable", "salary_percentile": 65},
    "Law": {"demand": 68, "growth_rate": 2, "trend": "declining", "salary_percentile": 78},
    "Psychology": {"demand": 72, "growth_rate": 5, "trend": "stable", "salary_percentile": 60}
}


# STUDENT SKILL ASSESSMENT

def assess_student_skills(student_profile: dict, level: str) -> Dict:
    """
    Assess which skills the student likely has based on their profile
    """
    skills_possessed = []
    
    if level == "OL":
        # O/L students - foundation level skills
        ol_passes = student_profile.get("ol_passes") or student_profile.get("passes", 0)
        
        # General foundation skills
        if ol_passes >= 5:
            skills_possessed.extend(["Academic Foundation", "Basic Learning Skills", "Study Discipline"])
        
        # English skills
        if student_profile.get("english", False):
            skills_possessed.extend(["English Communication", "Reading Comprehension", "Writing Ability", "Language Skills"])
        else:
            skills_possessed.append("Basic English")
        
        # Mathematics skills
        if student_profile.get("maths", False):
            skills_possessed.extend(["Mathematics", "Logical Thinking", "Numerical Ability", "Problem Solving Basics"])
        else:
            skills_possessed.append("Basic Numeracy")
        
        # Science skills
        if student_profile.get("science", False):
            skills_possessed.extend(["Scientific Thinking", "Experimental Understanding", "Technical Foundation", "Analysis Skills"])
        else:
            skills_possessed.append("Basic Science")
        
        # General characteristics
        skills_possessed.extend(["Adaptability", "Learning Aptitude", "Time Management"])
    
    elif level == "AL":
        # Check for strong math/science foundation
        if student_profile.get("maths", 0) >= 70:
            skills_possessed.extend(["Mathematics", "Logical Thinking", "Problem Solving", "Quantitative Analysis"])
        else:
            skills_possessed.extend(["Mathematics", "Logical Thinking"])
            
        if student_profile.get("english", 0) >= 70:
            skills_possessed.extend(["Communication", "Written Expression", "Analysis", "Critical Thinking"])
        else:
            skills_possessed.extend(["Communication", "Written Expression"])
            
        if student_profile.get("science", 0) >= 70:
            skills_possessed.extend(["Scientific Method", "Analysis", "Technical Foundation", "Research Skills"])
        else:
            skills_possessed.extend(["Scientific Method", "Basic Science Knowledge"])
        
        # Check AL subjects
        al_subject_1 = student_profile.get("al_subject_1", "").lower()
        al_score_1 = student_profile.get("al_score_1", 0)
        
        if any(kw in al_subject_1 for kw in ["it", "computing", "technology", "information"]):
            if al_score_1 >= 75:
                skills_possessed.extend(["Programming Basics", "Tech Literacy", "Digital Skills", "System Understanding"])
            else:
                skills_possessed.extend(["Tech Literacy", "Digital Skills"])
        
        if any(kw in al_subject_1 for kw in ["chemistry", "physics", "biology"]):
            if al_score_1 >= 75:
                skills_possessed.extend(["Laboratory Skills", "Experimental Design", "Data Interpretation"])
            else:
                skills_possessed.extend(["Laboratory Skills"])
        
        # Check preferences for additional skills
        preferences = student_profile.get("preferences", "").lower()
        if any(kw in preferences for kw in ["software", "development", "programming"]):
            skills_possessed.append("Software Development Interest")
        if any(kw in preferences for kw in ["data", "analytics", "business"]):
            skills_possessed.append("Data Analysis Interest")
    
    elif level == "BSC":
        degree_field = student_profile.get("degree_field", "").lower()
        if "computer" in degree_field or "software" in degree_field:
            skills_possessed.extend(["Programming", "Problem Solving", "System Design", "Code Quality", "Object-Oriented Design"])
        elif "data" in degree_field or "ai" in degree_field:
            skills_possessed.extend(["Statistics", "Python", "Machine Learning", "Data Analysis", "Mathematical Modeling"])
        elif "business" in degree_field:
            skills_possessed.extend(["Business Analysis", "Excel", "Strategic Thinking", "Communication", "Project Management"])
        
        if student_profile.get("english", 0) >= 70:
            skills_possessed.append("Professional Communication")
        
        skills_possessed.extend(["Research Skills", "Academic Writing"])
    
    elif level in ["HND", "DIPLOMA"]:
        field = student_profile.get("hnd_field") or student_profile.get("diploma_field", "")
        field_lower = field.lower()
        if "it" in field_lower or "computing" in field_lower:
            skills_possessed.extend(["Technical Support", "Basic Programming", "Troubleshooting", "Hardware Knowledge"])
        elif "business" in field_lower:
            skills_possessed.extend(["Office Management", "Customer Service", "Data Entry", "Business Communication"])
        elif "engineering" in field_lower:
            skills_possessed.extend(["CAD Software", "Technical Drawing", "Problem Solving"])
        
        skills_possessed.append("Practical Skills")
    
    elif level == "POSTGRAD":
        skills_possessed.extend(["Advanced Research", "Critical Analysis", "Subject Expertise", "Leadership", "Mentoring"])
    
    return {
        "possessed": list(set(skills_possessed)),
        "count": len(set(skills_possessed))
    }


# CAREER PATH PREDICTION

def predict_career_path(student_profile: dict, recommended_course: str, level: str) -> Dict:
    """
    Predict career progression based on student and course choice
    """
    # Determine field from course name - check most specific first!
    course_name_lower = recommended_course.lower()
    
    selected_field = None
    
    # Check MOST SPECIFIC categories FIRST to avoid false matches
    # 1. Healthcare (MOST SPECIFIC - check first to avoid false positives)
    if any(kw in course_name_lower for kw in ["pharmaceutical", "pharmacy", "medical", "nursing", "health", "medicine", "biomedical", "clinical", "dental", "cosmetic science", "midwife"]):
        selected_field = "healthcare"
    
    # 2. Data Science (check for EXACT PHRASES to avoid "cadet" matching "ai")
    elif ("data" in course_name_lower or "analytics" in course_name_lower or 
          "artificial intelligence" in course_name_lower or "machine learning" in course_name_lower or
          "ml engineer" in course_name_lower or "data science" in course_name_lower):
        selected_field = "data-science"
    
    # 3. Education/Teaching
    elif any(kw in course_name_lower for kw in ["teaching", "education", "tesol", "english diploma"]):
        selected_field = "business-management"  # Use business-management for education
    
    # 4. Business (check specific keywords before general terms)
    elif any(kw in course_name_lower for kw in ["business", "commerce", "finance", "accounting", "marketing", "entrepreneurship", "hospitality", "hotel", "tourism", "management", "hr management"]):
        selected_field = "business-management"
    
    # 5. Psychology
    elif any(kw in course_name_lower for kw in ["psychology"]):
        selected_field = "business-management"  # Use business-management for psychology
    
    # 6. Cyber Security / Network (specific security keywords)
    elif any(kw in course_name_lower for kw in ["cyber", "security", "network computing", "information security"]):
        selected_field = "software-engineering"
    
    # 7. Software Engineering (check specific software/development keywords)
    elif any(kw in course_name_lower for kw in ["software", "development", "developer", "programming", "computer science", "cloud", "web development", "ict", "it"]):
        selected_field = "software-engineering"
    
    # 8. Engineering (mechanical, electrical, civil etc)
    elif any(kw in course_name_lower for kw in ["mechanical engineering", "electrical engineering", "electronic engineering", "civil engineering", "quantity surveying", "beng"]):
        selected_field = "software-engineering"
    
    # Default: if no specific match found, use business as safer default than software
    if selected_field is None:
        selected_field = "business-management"
    
    career_path = CAREER_PATHS.get(selected_field, CAREER_PATHS["software-engineering"])
    
    return {
        "field": selected_field,
        "field_name": selected_field.replace("-", " ").title(),
        "current_level": level,
        "progression": career_path["progression"],
        "career_options": career_path["careers"],
        "recommended_next_step": career_path["progression"][0] if level == "AL" else career_path["progression"][min(1, len(career_path["progression"])-1)]
    }

# =====================================================
# SKILL GAP ANALYSIS
# =====================================================
def analyze_skill_gaps(student_profile: dict, target_course: str, level: str) -> Dict:
    """
    Analyze which skills student needs for the course - uses intelligent skill mapping
    """
    # Try to match course name to skill category first
    course_lower = target_course.lower()
    required_skills = []
    
    # Intelligent skill mapping - check MOST SPECIFIC FIRST!
    # 1. Healthcare (very specific)
    if any(kw in course_lower for kw in ["health", "medical", "nursing", "pharmacy", "biomedical", "clinical"]):
        required_skills = COURSE_SKILLS.get("Healthcare", [])
    
    # 2. Civil/Mechanical Engineering (specific)
    elif any(kw in course_lower for kw in ["civil engineering", "mechanical engineering", "quantity surveying"]):
        required_skills = COURSE_SKILLS.get("Civil Engineering", [])
    
    # 3. Data Science (before general software to avoid false matches)
    elif any(kw in course_lower for kw in ["data", "analytics", "ai", "artificial", "machine learning", "intelligence", "ml"]):
        required_skills = COURSE_SKILLS.get("Data Science", [])
    
    # 4. Education/Teaching
    elif any(kw in course_lower for kw in ["teaching", "education", "tesol", "english diploma"]):
        required_skills = COURSE_SKILLS.get("Education", [])
    
    # 5. Psychology
    elif any(kw in course_lower for kw in ["psychology"]):
        required_skills = COURSE_SKILLS.get("Psychology", [])
    
    # 6. Hospitality/Hotel Management
    elif any(kw in course_lower for kw in ["hospitality", "hotel management", "catering"]):
        required_skills = COURSE_SKILLS.get("Hospitality", [])
    
    # 7. Tourism
    elif any(kw in course_lower for kw in ["tourism"]):
        required_skills = COURSE_SKILLS.get("Tourism", [])
    
    # 8. Business (before general software/engineer)
    elif any(kw in course_lower for kw in ["business", "management", "commerce", "finance", "accounting", "marketing", "entrepreneurship"]):
        required_skills = COURSE_SKILLS.get("Business Management", [])
    
    # 9. Engineering courses (mechanical, electrical - specific)
    elif any(kw in course_lower for kw in ["mechanical", "electrical", "electronic"]):
        required_skills = COURSE_SKILLS.get("Engineering", [])
    
    # 10. Software Engineering (broader tech match)
    elif any(kw in course_lower for kw in ["software", "development", "developer", "programming", "computer science", "cloud", "cyber", "security", "ict", "it"]):
        required_skills = COURSE_SKILLS.get("Software Engineering", [])
    
    else:
        # Fallback to course name match
        required_skills = COURSE_SKILLS.get(target_course, COURSE_SKILLS.get("Business Management", []))
    
    
    student_skills = assess_student_skills(student_profile, level)
    possessed = student_skills["possessed"]
    
    # Calculate gaps with improved matching
    skill_gaps = []
    for skill in required_skills:
        # More intelligent matching: check for keyword overlaps
        skill_keywords = skill.lower().split()
        is_possessed = False
        
        for possessed_skill in possessed:
            possessed_keywords = possessed_skill.lower().split()
            # Check if any significant keyword matches
            common_keywords = set(skill_keywords) & set(possessed_keywords)
            if common_keywords:
                is_possessed = True
                break
            
            # Also check for substring matches for keywords
            if any(keyword in possessed_skill.lower() for keyword in skill_keywords if len(keyword) > 3):
                is_possessed = True
                break
        
        if not is_possessed:
            skill_gaps.append(skill)
    
    # Calculate readiness score - based on possession percentage
    if required_skills:
        readiness_score = max(0, min(100, ((len(required_skills) - len(skill_gaps)) / len(required_skills) * 100)))
    else:
        readiness_score = 65  # Neutral default
    
    # Recommend prerequisites based on gaps
    prerequisites = []
    if len(skill_gaps) > 3:
        prerequisites.append({
            "course": "Foundation Courses",
            "reason": "Strong foundational gaps detected",
            "duration": "2-3 months"
        })
    elif len(skill_gaps) > 1:
        prerequisites.append({
            "course": "Preparatory Modules",
            "reason": "Some skill gaps detected",
            "duration": "1-2 months"
        })
    
    return {
        "course": target_course,
        "required_skills": required_skills if required_skills else ["Critical Thinking", "Problem Solving", "Continuous Learning"],
        "possessed_skills": possessed,
        "skill_gaps": skill_gaps,
        "gaps_count": len(skill_gaps),
        "readiness_score": readiness_score,
        "readiness_level": "Highly Ready" if readiness_score > 80 else "Ready" if readiness_score > 60 else "Needs Preparation" if readiness_score > 40 else "Requires Foundation",
        "prerequisites": prerequisites
    }

# =====================================================
# JOB MARKET ALIGNMENT
# =====================================================
def calculate_job_market_alignment(course_field: str, student_profile: dict) -> Dict:
    """
    Score courses based on current job market demand and trends
    """
    # Normalize field name for lookup
    field_lookup = course_field.title() if isinstance(course_field, str) else "Software Engineering"
    
    # Handle different field name formats
    if "software" in field_lookup.lower() or "development" in field_lookup.lower():
        field_lookup = "Software Engineering"
    elif "data" in field_lookup.lower():
        field_lookup = "Data Science"
    elif "cyber" in field_lookup.lower() or "security" in field_lookup.lower():
        field_lookup = "Cybersecurity"
    elif "cloud" in field_lookup.lower():
        field_lookup = "Cloud Computing"
    elif "business" in field_lookup.lower():
        field_lookup = "Business Management"
    
    market_data = JOB_MARKET.get(field_lookup, {
        "demand": 75,
        "growth_rate": 5,
        "trend": "stable",
        "salary_percentile": 65
    })
    
    # Calculate alignment score
    demand_score = market_data["demand"]  # 0-100
    growth_score = min(100, market_data["growth_rate"] * 7)  # Normalize growth rate
    alignment_score = (demand_score * 0.6) + (growth_score * 0.4)
    
    # Trend indicators
    trend_emoji = {
        "rapidly-growing": "🚀",
        "growing": "📈",
        "stable": "➡️",
        "declining": "📉"
    }
    
    return {
        "field": field_lookup,
        "demand_score": demand_score,
        "growth_rate": market_data["growth_rate"],
        "trend": market_data["trend"],
        "trend_icon": trend_emoji.get(market_data["trend"], "➡️"),
        "alignment_score": round(alignment_score, 1),
        "salary_percentile": market_data["salary_percentile"],
        "insight": f"High demand in job market with {market_data['growth_rate']}% annual growth",
        "recommendation": "Excellent choice for career prospects" if alignment_score > 80 else "Good job market opportunity" if alignment_score > 60 else "Consider market demand"
    }

# =====================================================
# COMPREHENSIVE AI ANALYSIS
# =====================================================
def generate_ai_insights(student_profile: dict, recommended_courses: List[dict], level: str) -> Dict:
    """
    Generate comprehensive AI insights for all 3 features
    """
    insights = {
        "timestamp": datetime.now().isoformat(),
        "student_level": level,
        "analysis": []
    }
    
    for i, course in enumerate(recommended_courses[:3]):  # Top 3 courses
        course_name = course.get("course_name", "Unknown Course")
        
        # Career path
        career_path = predict_career_path(student_profile, course_name, level)
        
        # Skill gaps
        skill_gaps = analyze_skill_gaps(student_profile, course_name, level)
        
        # Job market - use the field from career path
        field = career_path.get("field_name", "Software Engineering")  # Use field_name directly
        job_market = calculate_job_market_alignment(field, student_profile)
        
        insights["analysis"].append({
            "rank": i + 1,
            "course": course_name,
            "match_score": course.get("final_score", 0),
            "career_path": career_path,
            "skill_gaps": skill_gaps,
            "job_market": job_market
        })
    
    return insights

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.schemas import *
from api.recommender import recommend_courses
from api.ai_features import generate_ai_insights

app = FastAPI(title="Sri Lanka Course Recommender with AI Features")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/recommend/ol")
def recommend_ol(student: OLStudent):
    recommendations = recommend_courses(student, level="OL")
    # Add AI insights
    if recommendations.get("recommendations"):
        ai_insights = generate_ai_insights(
            student.dict(),
            recommendations.get("recommendations", []),
            "OL"
        )
        recommendations["ai_insights"] = ai_insights
    return recommendations

@app.post("/recommend/al")
def recommend_al(student: ALStudent):
    recommendations = recommend_courses(student, level="AL")
    if recommendations.get("recommendations"):
        ai_insights = generate_ai_insights(
            student.dict(),
            recommendations.get("recommendations", []),
            "AL"
        )
        recommendations["ai_insights"] = ai_insights
    return recommendations

@app.post("/recommend/diploma")
def recommend_diploma(student: DiplomaStudent):
    recommendations = recommend_courses(student, level="DIPLOMA")
    if recommendations.get("recommendations"):
        ai_insights = generate_ai_insights(
            student.dict(),
            recommendations.get("recommendations", []),
            "DIPLOMA"
        )
        recommendations["ai_insights"] = ai_insights
    return recommendations

@app.post("/recommend/hnd")
def recommend_hnd(student: HNDStudent):
    recommendations = recommend_courses(student, level="HND")
    if recommendations.get("recommendations"):
        ai_insights = generate_ai_insights(
            student.dict(),
            recommendations.get("recommendations", []),
            "HND"
        )
        recommendations["ai_insights"] = ai_insights
    return recommendations

@app.post("/recommend/bsc")
def recommend_bsc(student: BScStudent):
    recommendations = recommend_courses(student, level="BSC")
    if recommendations.get("recommendations"):
        ai_insights = generate_ai_insights(
            student.dict(),
            recommendations.get("recommendations", []),
            "BSC"
        )
        recommendations["ai_insights"] = ai_insights
    return recommendations

@app.post("/recommend/postgrad")
def recommend_postgrad(student: PostgradStudent):
    recommendations = recommend_courses(student, level="POSTGRAD")
    if recommendations.get("recommendations"):
        ai_insights = generate_ai_insights(
            student.dict(),
            recommendations.get("recommendations", []),
            "POSTGRAD"
        )
        recommendations["ai_insights"] = ai_insights
    return recommendations

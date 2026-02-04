# UniMatch — Intelligent University Recommendation System 🎓✨

An AI-powered decision support system that intelligently recommends university courses based on academic background, eligibility criteria, and career alignment.  
The system scrapes course data from partner institutions, normalizes and enriches it, generates semantic embeddings, and delivers personalized recommendations via a FastAPI backend and a React (Vite) frontend.

---

## 🚀 Quick Links
- Backend (FastAPI): `api/`
- Frontend (React + Vite): `frontend/`
- Scraper & normalization: `main.py`, `crawler/`, `extractor/`, `normalizer/`
- Database helpers: `db/mongodb.py`
- Documentation & media: `DOCS/`

---

## 📸 Screenshots

### Home / Landing Page
![Home Screen](DOCS/media/screenshots/home.png)

### Course Recommendations
![Recommendations](DOCS/media/screenshots/recommendations-1.png)
![Recommendations](DOCS/media/screenshots/recommendations-2.png)

### Additional Views
![AI Insights](DOCS/media/screenshots/ai-insights.png)
![University List](DOCS/media/screenshots/university-list.png)

---

## 🎥 Demo Video

<video controls width="720">
  <source src="DOCS/media/video/demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

---

## 🧩 Key Features
- Scrapes course pages from multiple Sri Lankan universities (extensible design)
- Sitemap-based crawling with robots.txt compliance
- Robust HTML downloading with retry and rate-limiting
- Site-specific extractors with a shared base interface
- Course data normalization (duration, eligibility, metadata)
- Semantic similarity using sentence embeddings
- AI-powered insights:
  - Career path prediction
  - Skill gap analysis
  - Job market alignment
- RESTful API with FastAPI and Pydantic schemas
- Modern frontend built with React, Vite, and Tailwind
- CSV export utilities for offline analysis

---

## ✅ Prerequisites
- Python 3.10+ (Windows tested)
- Node.js 18+ and npm
- MongoDB (local or remote)
- Internet access for embedding model download (or local model path)

---

## 🔧 Backend Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

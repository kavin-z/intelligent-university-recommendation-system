# UniMatch — University Course Scraper & Recommender 🎓✨

> Find your dream course in seconds. Scrapes course pages from partner institutions, normalizes course data, builds embeddings, and serves AI-powered course recommendations via a FastAPI backend and a React frontend.

---

## 🚀 Quick Links
- Project root: `./`
- Backend (FastAPI): `api/`
- Frontend (React + Vite): `frontend/`
- Scraper & normalization: `main.py`, `extractor/`, `normalizer/`
- DB helpers: `db/mongodb.py`
- Place media in: `DOCS/media/` (see below)

---

## 📸 Screenshots & Demo Video ✅
Below are the screenshots and the demo video you provided (copied into `DOCS/media/`). They are embedded so they display clearly in this README.

**Screenshots**

- **Home screen**

  <img src="./DOCS/media/screenshots/home.png" alt="Home Screen" width="840" />

- **Course / Recommender (gallery)**

  <img src="./DOCS/media/screenshots/course_recommender_1.png" alt="Recommender 1" width="420" />
  <img src="./DOCS/media/screenshots/course_recommender_2.png" alt="Recommender 2" width="420" />

- **Extra screenshots**

  <img src="./DOCS/media/screenshots/extra_1.png" alt="Extra 1" width="420" />
  <img src="./DOCS/media/screenshots/extra_2.png" alt="Extra 2" width="420" />

**Demo video**

<!-- Use a clickable thumbnail that links to the local video file. Many renderers (including GitHub) don't reliably play local <video> tags inline, so we link directly. -->

<a href="./DOCS/media/video/demo.mp4">
  <img src="./DOCS/media/screenshots/home.png" alt="Play demo video (click to open)" width="840" />
</a>


**Notes:**
- If the images still appear as links in your editor preview, try opening the image file directly (right-click → "Open") to confirm it displays.  
- GitHub's README rendering does not support inline playback of local videos; upload the demo to YouTube/Vimeo for inline web playback or provide a GIF thumbnail for quick previews.

---

## 🔧 Backend API URL
- Interactive docs: http://127.0.0.1:8000/docs

---

## 🧭 AI Pipeline Architecture 🔬

![AI Pipeline](DOCS/media/ai_pipeline.svg)

**Overview:** Data is crawled from university websites and sitemaps, downloaded and parsed by per-university extractors, normalized and stored in MongoDB. Course text is encoded into embeddings (Sentence-BERT), which power the vector search used by the Recommender API. AI modules provide additional insights (career paths, skill gaps) that are returned with recommendations.

---

## 👨‍💻 Maintainer & Contact
- **Name:** M. Kavin
- **Degree:** BSc in Software Engineering
- **University:** ICBT
- **Email:** [mohanarajkavin@gmail.com](mailto:mohanarajkavin@gmail.com)
- **GitHub:** https://github.com/kavin-z

---

## 🧩 Features
- Scrapes course pages from 12+ Sri Lankan universities (extensible)
- Normalizes course metadata (name, description, fees, duration, keywords)
- Generates sentence embeddings for semantic matching (`api/generate_embeddings.py`)
- AI features: career path prediction, skill-gap analysis, job-market alignment (`api/ai_features.py`)
- Recommender endpoints for multiple student types (OL, AL, Diploma, HND, BSc, Postgrad)
- Frontend UI (React + Vite) with course / university browsing
- Export courses to CSV: `scripts/export_courses_to_csv.py`

---

## ✅ Prerequisites
- Python 3.10+ (Windows tested)
- Node.js 18+ & npm/yarn (for frontend)
- MongoDB (local or remote) or Docker
- Internet access for downloading embedding models (or set a local model path)

---

## 🔧 Backend Setup
1. Create and activate a virtual environment (PowerShell):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
2. Install Python dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Optional environment variables (defaults shown):
   - `MONGO_URI` — default: `mongodb://localhost:27017`
   - `EMBEDDING_MODEL_NAME` — default: `all-MiniLM-L6-v2`
   - `EMBEDDING_MODEL_PATH` — set to a local model directory if offline
4. Start the API (development):
   ```powershell
   uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
   ```
5. Open the interactive API docs at: `http://127.0.0.1:8000/docs`

---

## 🧭 Frontend Setup
1. Install frontend deps and start dev server:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
2. Open the Vite dev URL (usually `http://localhost:5173`).

---

## 🛠 Scraping & Data
- Run the scraper (iterates `config/universities.json` and saves to MongoDB):
  ```bash
  python main.py
  ```
- Export DB to CSV:
  ```bash
  python scripts/export_courses_to_csv.py
  # Produces: courses_raw.csv
  ```

---

## 🧠 Embeddings & AI
- Generate embeddings for all courses (required for semantic matching):
  ```bash
  python api/generate_embeddings.py
  ```
- The script uses `sentence-transformers`. If you're offline, set `EMBEDDING_MODEL_PATH` to a local model directory.

---

## 🔬 API Usage Examples
- AL student example (POST `/recommend/al`):

  ```json
  {
    "stream": "Science",
    "al_passes": 3,
    "english": true
  }
  ```

- OL student example (POST `/recommend/ol`):

  ```json
  {
    "english": true,
    "maths": true,
    "science": true,
    "passes": 6
  }
  ```

Use the interactive docs at `/docs` to see the exact Pydantic schemas from `api/schemas.py`.

---

## 📁 Project Layout (short)
- `api/` — FastAPI endpoints, recommender, embeddings, AI features
- `extractor/` — University-specific extractors
- `downloader/` — HTML downloader utilities
- `crawler/` — URL discovery and sitemap parsing
- `normalizer/` — course normalization logic
- `db/` — MongoDB helper functions
- `frontend/` — React + Vite UI
- `scripts/` — export & helper scripts
- `DOCS/` — documentation and media (put screenshots & video here)

---

## 🧰 Development & Contributing
- Use feature branches and open pull requests for changes.
- Add extractor test inputs (sample HTML) when adding support for new universities.
- Lint frontend: `cd frontend && npm run lint`.

---

## ⚠️ Troubleshooting
- MongoDB: ensure service is running or update `MONGO_URI` in your environment.
- Embedding model errors offline: set `EMBEDDING_MODEL_PATH` to a local model dir.
- Frontend CORS: API allows `http://localhost:5173` by default in `api/main.py`.

---

## 🧾 License & Contact
- Add a `LICENSE` file (e.g., MIT) and your contact details to the repo.

---

## ✅ Next steps
1. Upload your screenshots to `DOCS/media/screenshots/` and the demo video to `DOCS/media/video/` (or provide a public link).  
2. Tell me the filenames and I will update the README to embed them and commit the changes.

---

*README generated and ready. Tell me the filenames for the screenshots and demo video and I will insert them into this document and commit the files.*

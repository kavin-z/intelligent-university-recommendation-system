from pymongo import MongoClient
import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np
import os


# Load ML model once

MODEL_PATH = "testing/eligibility_model.pkl"
model = joblib.load(MODEL_PATH)


# AI Embedding model (lazy load + optional local path via EMBEDDING_MODEL_PATH)
EMBEDDING_MODEL = None

def get_embedding_model():
    """Return a cached SentenceTransformer instance or try to load it.

    Set EMBEDDING_MODEL_PATH to a local directory containing the model to avoid
    network access, or set EMBEDDING_MODEL_NAME to specify a different HF model.
    """
    global EMBEDDING_MODEL
    if EMBEDDING_MODEL is not None:
        return EMBEDDING_MODEL

    model_name = os.environ.get("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
    local_path = os.environ.get("EMBEDDING_MODEL_PATH")

    try:
        if local_path:
            print(f"Loading Sentence-BERT model from local path: {local_path}")
            EMBEDDING_MODEL = SentenceTransformer(local_path)
        else:
            # Respect offline flags to avoid long network retries
            if os.environ.get("HF_HUB_OFFLINE") == "1" or os.environ.get("TRANSFORMERS_OFFLINE") == "1":
                print("⚠️ HF_HUB_OFFLINE or TRANSFORMERS_OFFLINE is set; skipping remote model download.")
                EMBEDDING_MODEL = None
            else:
                print(f"Loading Sentence-BERT model: {model_name}")
                EMBEDDING_MODEL = SentenceTransformer(model_name)
        if EMBEDDING_MODEL:
            print("AI model loaded successfully!")
        else:
            print("⚠️ Embedding model not loaded (running without AI).")
    except Exception as e:
        # Keep service running but disable semantic search
        print(f"⚠️ Failed to load embedding model ({model_name}): {e}")
        EMBEDDING_MODEL = None
    return EMBEDDING_MODEL

# =====================================================
# MongoDB
# =====================================================
client = MongoClient("mongodb://localhost:27017")
db = client["ugc_scraper"]
courses_col = db["courses"]

# =====================================================
# Student normalization (SAFE)
# =====================================================
def normalize_student(student, level):
    return {
        "english": getattr(student, "english", False),
        "maths": getattr(student, "maths", False),
        "science": getattr(student, "science", False),
        "al_passes": getattr(student, "al_passes", 0),
        "ol_passes": getattr(student, "passes", 0),
        "stream": getattr(student, "stream", None),
        "hnd_field": getattr(student, "hnd_field", None),
        "diploma_field": getattr(student, "diploma_field", None),
        "degree_field": getattr(student, "degree_field", None),
        "postgrad_field": getattr(student, "postgrad_field", None),
        "level": level
    }

# =====================================================
# AI SEMANTIC SEARCH
# =====================================================
def semantic_course_search(student_vec, level):
    """
    AI-powered semantic search for courses using sentence embeddings
    """
    try:
        # Create student profile text based on level
        if level == "OL":
            ol_passes = student_vec.get("ol_passes", 0)
            profile = f"O/L student with {ol_passes} passes looking for foundation certificate or diploma programs"
        elif level == "AL":
            stream = student_vec.get("stream", "general")
            al_passes = student_vec.get("al_passes", 0)
            profile = f"A/L {stream} stream student with {al_passes} passes seeking undergraduate degree bachelor programs"
        elif level == "DIPLOMA":
            field = student_vec.get("diploma_field", "general")
            profile = f"Diploma graduate in {field} looking for advanced diploma or bachelor degree programs"
        elif level == "HND":
            field = student_vec.get("hnd_field", "general")
            profile = f"HND graduate in {field} seeking top-up degree or bachelor programs"
        elif level == "BSC":
            field = student_vec.get("degree_field", "general")
            profile = f"Bachelor degree holder in {field} looking for postgraduate masters programs"
        elif level == "POSTGRAD":
            field = student_vec.get("postgrad_field", "general")
            profile = f"Postgraduate applicant in {field} seeking masters MBA MSc or PhD programs"
        else:
            profile = "Student looking for suitable courses"
        
        # Generate student profile embedding
        model = get_embedding_model()
        if model is None:
            print("⚠️ Embedding model unavailable; skipping semantic search.")
            return None
        student_embedding = model.encode(profile)
        
        # Get all courses with embeddings
        courses = list(courses_col.find({"embedding": {"$exists": True}}))
        
        if not courses:
            print("⚠️ No course embeddings found. Returning all courses.")
            return None
        
        # Calculate semantic similarity scores
        similarities = []
        for course in courses:
            try:
                course_embedding = np.array(course["embedding"])
                # Cosine similarity
                similarity = np.dot(student_embedding, course_embedding) / (
                    np.linalg.norm(student_embedding) * np.linalg.norm(course_embedding)
                )
                course["semantic_score"] = float(similarity)
                similarities.append(course)
            except:
                # If embedding is invalid, skip this course
                continue
        
        # Sort by semantic similarity
        similarities.sort(key=lambda x: x.get("semantic_score", 0), reverse=True)
        
        print(f"🤖 AI found {len(similarities)} semantically relevant courses")
        return similarities[:100]  # Return top 100 for further filtering
        
    except Exception as e:
        print(f"⚠️ Error in semantic search: {e}")
        import traceback
        traceback.print_exc()
        return None

# =====================================================
# MAIN RECOMMENDER
# =====================================================
def recommend_courses(student, level):
    student_vec = normalize_student(student, level)

    # -------------------------
    # AI-Powered Semantic Search (Step 1)
    # -------------------------
    print("🤖 Running AI semantic course matching...")
    semantic_results = semantic_course_search(student_vec, level)
    
    if semantic_results:
        # Use AI-filtered courses
        df = pd.DataFrame(semantic_results)
        print(f"✅ AI pre-filtered to {len(df)} relevant courses")
    else:
        # Fallback to all courses if AI fails
        print("⚠️ Using traditional search (AI unavailable)")
        courses = list(courses_col.find())
        df = pd.DataFrame(courses)
        df["semantic_score"] = 0.5  # Neutral score for fallback

    if df.empty:
        return {
            "level": level,
            "recommendations": []
        }

    # -------------------------
    # LEVEL-BASED HARD FILTERING (CRITICAL)
    # -------------------------
    if level == "OL":
        # More realistic O/L filtering based on number of passes
        ol_passes = student_vec.get("ol_passes", 0)
        
        # Filter courses based on O/L pass count
        if ol_passes >= 6:
            # 6+ passes: Foundation, Certificate, Diploma (basic/general), NVQ Level 3-5
            df = df[df["course_name"].str.contains(
                "Foundation|Certificate|Diploma|NVQ|Vocational|Professional Certificate|Entry Level|Pre-University",
                case=False, na=False
            )]
        elif ol_passes >= 4:
            # 4-5 passes: Certificate, NVQ Level 2-4, Basic Diploma
            df = df[df["course_name"].str.contains(
                "Certificate|Diploma|NVQ|Vocational|Basic|Professional Certificate|Skills",
                case=False, na=False
            )]
        else:
            # 0-3 passes: Basic Certificate, NVQ Level 1-2, Vocational Training
            df = df[df["course_name"].str.contains(
                "Certificate|NVQ|Vocational|Basic|Skills|Training|Entry",
                case=False, na=False
            )]
        
        # CRITICAL: Exclude all higher-level programs (but NOT regular diplomas)
        # Use word boundaries (\b) to be more precise
        df = df[~df["course_name"].str.contains(
            r"\bBachelor\b|\bBSc\b|\bBA\b|\bBBA\b|\bBEng\b|\bMaster\b|\bMSc\b|\bMA\b|\bMBA\b|\bPhD\b|\bDoctor\b|\bDoctorate\b|\bPostgraduate\b|Top-up|Top Up",
            case=False, na=False, regex=True
        )]
        
        # Exclude ONLY advanced diploma types (HND, Higher Diploma, Advanced Diploma)
        # These patterns are specific enough to not catch regular "Diploma"
        df = df[~df["course_name"].str.contains(
            r"\bHND\b|Higher\s+National\s+Diploma|Higher\s+Diploma|Advanced\s+Diploma",
            case=False, na=False, regex=True
        )]
        
        # Subject-specific filtering for better matching
        has_english = student_vec.get("english", False)
        has_maths = student_vec.get("maths", False)
        has_science = student_vec.get("science", False)
        
        # If student lacks key subjects, exclude programs that heavily require them
        if not has_english:
            df = df[~df["course_name"].str.contains(
                "English Language|Communication Studies|Media|Journalism",
                case=False, na=False
            )]
        
        if not has_maths:
            df = df[~df["course_name"].str.contains(
                "Engineering|Mathematics|Accounting|Finance|Computer Science|Programming",
                case=False, na=False
            )]
        
        if not has_science:
            df = df[~df["course_name"].str.contains(
                "Science|Medical|Nursing|Pharmacy|Laboratory|Biotechnology",
                case=False, na=False
            )]

    elif level == "AL":
        # A/L students should see undergraduate degree programs only
        # Include: Bachelor's degrees, BSc, BA, BBA, BEng, undergraduate programs
        df = df[df["course_name"].str.contains(
            r"\bBachelor\b|\bBSc\b|\bBA\b|\bBBA\b|\bBEng\b|\bBTech\b|Undergraduate|Degree Program",
            case=False, na=False, regex=True
        )]
        
        # Exclude postgraduate programs
        df = df[~df["course_name"].str.contains(
            r"\bPhD\b|\bDoctor\b|\bMSc\b|\bMaster\b|\bMBA\b|\bPostgraduate\b",
            case=False, na=False, regex=True
        )]
        
        # Exclude entry-level programs (those are for O/L students)
        df = df[~df["course_name"].str.contains(
            r"\bFoundation\b|\bCertificate\b|Entry Level|Pre-University",
            case=False, na=False, regex=True
        )]
        
        # Filter by AL stream if provided
        if student_vec.get("stream"):
            stream = student_vec["stream"].lower()
            
            if stream == "science":
                df = df[df["course_name"].str.contains(
                    r"Computing|Computer|Software|Engineering|Science|Technology|Medicine|Health|Cyber|Data|\bIT\b|Information Technology|Biotechnology|Architecture|Pharmacy|Medical|Nursing",
                    case=False, na=False, regex=True
                )]
            elif stream == "commerce":
                df = df[df["course_name"].str.contains(
                    r"Business|Accounting|Finance|Economics|Management|Marketing|Commerce|\bBBA\b|Banking|Entrepreneurship|Business Administration",
                    case=False, na=False, regex=True
                )]
            elif stream == "arts":
                df = df[df["course_name"].str.contains(
                    r"Arts|Psychology|Law|Media|Communication|Humanities|Social|Education|Counseling|English|History|Sociology|Political|\bLLB\b|Legal Studies",
                    case=False, na=False, regex=True
                )]
            elif stream == "technology":
                df = df[df["course_name"].str.contains(
                    r"Technology|Engineering|Computing|Computer|Software|\bIT\b|Information Technology|Cyber|Data|Network|Electronics|Telecommunications",
                    case=False, na=False, regex=True
                )]
            elif stream == "maths":
                df = df[df["course_name"].str.contains(
                    r"Mathematics|Statistics|Actuarial|Data Science|Computing|Computer|Software|Engineering|Physics|Economics|Finance|Quantitative",
                    case=False, na=False, regex=True
                )]

    elif level == "DIPLOMA":
        # Diploma holders should see HND, Bachelor's and Master's programs
        # Include: HND, Bachelor's degrees and Master's programs
        df = df[df["course_name"].str.contains(
            r"\bHND\b|Higher National Diploma|\bBachelor\b|\bBSc\b|\bBA\b|\bBBA\b|\bBEng\b|\bBTech\b|\bMSc\b|\bMA\b|\bMBA\b|\bMaster\b|Postgraduate|Undergraduate|Degree Program",
            case=False, na=False, regex=True
        )]
        
        # Exclude PhD/Doctorate and entry-level programs (but NOT HND or Diploma)
        df = df[~df["course_name"].str.contains(
            r"\bPhD\b|\bDoctor\b|\bDoctorate\b|\bFoundation\b|\bCertificate\b|\bNVQ\b|Entry Level|Pre-University|Vocational Training",
            case=False, na=False, regex=True
        )]
    
    elif level == "HND":
        # HND holders should see Bachelor's (Degree) and Master's programs ONLY
        # Include: Bachelor's degrees and Master's programs
        df = df[df["course_name"].str.contains(
            r"\bBachelor\b|\bBSc\b|\bBA\b|\bBBA\b|\bBEng\b|\bBTech\b|\bMSc\b|\bMA\b|\bMBA\b|\bMaster\b|Postgraduate|Undergraduate|Degree Program",
            case=False, na=False, regex=True
        )]
        
        # Exclude PhD/Doctorate, Diplomas, and entry-level programs
        df = df[~df["course_name"].str.contains(
            r"\bPhD\b|\bDoctor\b|\bDoctorate\b|\bDiploma\b|\bHND\b|\bFoundation\b|\bCertificate\b|\bNVQ\b|Entry Level|Pre-University|Vocational Training",
            case=False, na=False, regex=True
        )]
    
    elif level == "BSC":
        # BSC holders (already have Bachelor's) should see ONLY Master's programs
        # Include Master's, MSc, MA, MBA, Postgraduate
        df = df[df["course_name"].str.contains(
            r"\bMSc\b|\bMA\b|\bMBA\b|\bMaster\b|Postgraduate|Post Graduate",
            case=False, na=False, regex=True
        )]
        
        # Exclude PhD/Doctorate and Bachelor's programs
        df = df[~df["course_name"].str.contains(
            r"\bPhD\b|\bDoctor\b|\bDoctorate\b|\bBachelor\b|\bBSc\b|\bBA\b|\bBBA\b|\bBEng\b|\bBTech\b",
            case=False, na=False, regex=True
        )]
        
        # Exclude entry-level programs
        df = df[~df["course_name"].str.contains(
            r"\bFoundation\b|\bCertificate\b|\bDiploma\b|\bHND\b|\bNVQ\b|Entry Level|Pre-University|Vocational Training",
            case=False, na=False, regex=True
        )]
        
        # Field-based filtering for HND
        if level == "HND" and student_vec.get("hnd_field"):
            field = student_vec["hnd_field"].lower()
            
            # First, exclude IT courses globally for non-IT fields to prevent leakage
            if "computing" not in field and "it" not in field:
                df = df[~df["course_name"].str.contains(
                    r"\bIT\b|Information Technology|Computing|Computer Science|Software Engineering|Programming|Data Science|Cyber Security|Network|Systems|Database|Cloud Computing|DevOps|\bAI\b|Artificial Intelligence|Machine Learning|Web Development",
                    case=False, na=False, regex=True
                )]
            
            if "computing" in field or "it" in field:
                df = df[df["course_name"].str.contains(
                    r"Computing|Computer|Software|\bIT\b|Information Technology|Cyber|Data Science|Network|Programming|Web Development|IT Management|Systems|Database|Cloud|DevOps|\bAI\b|Artificial Intelligence|Machine Learning",
                    case=False, na=False, regex=True
                )]
            elif "business" in field:
                df = df[df["course_name"].str.contains(
                    r"Business|\bBBA\b|Entrepreneurship|Commerce|Business Administration|Corporate Strategy|Business Analytics|Supply Chain",
                    case=False, na=False, regex=True
                )]
            elif "engineering" in field:
                df = df[df["course_name"].str.contains(
                    r"Engineering|Technology|Architecture|Construction|Civil|Mechanical|Electrical|Electronic|Chemical|Industrial|Structural|Building|Quantity Survey",
                    case=False, na=False, regex=True
                )]
            elif "health" in field:
                df = df[df["course_name"].str.contains(
                    r"Health|Medicine|Nursing|Pharmacy|Medical|Clinical|Healthcare|Public Health|Biomedical|Physiotherapy|Nutrition|Epidemiology|Health Sciences",
                    case=False, na=False, regex=True
                )]

            elif "arts" in field or "design" in field:
                df = df[df["course_name"].str.contains(
                    r"Arts|Design|Creative|Graphics|Media|Visual|Interior|Fashion|Animation|Illustration|Fine Arts|Digital Arts|\bUX\b|\bUI\b",
                    case=False, na=False, regex=True
                )]
            elif "accounting" in field or "finance" in field:
                df = df[df["course_name"].str.contains(
                    r"Accounting|Finance|Banking|Economics|Financial|Audit|Taxation|ACCA|CIMA|CMA|Investment|Treasury",
                    case=False, na=False, regex=True
                )]
            elif "marketing" in field:
                df = df[df["course_name"].str.contains(
                    r"Marketing|Sales|Digital Marketing|Brand|Advertising|Consumer|Market Research|Social Media Marketing|Content Marketing",
                    case=False, na=False, regex=True
                )]
            elif "management" in field:
                df = df[df["course_name"].str.contains(
                    r"Management|Leadership|Administration|Strategic|Operations|Project Management|Human Resource|\bHRM\b|Organizational|Executive",
                    case=False, na=False, regex=True
                )]
            elif "psychology" in field:
                df = df[df["course_name"].str.contains(
                    r"Psychology|Counseling|Mental Health|Behavioral|Clinical Psychology|Cognitive|Developmental|Social Psychology|Psychotherapy|Psychiatric",
                    case=False, na=False, regex=True
                )]
            elif "education" in field:
                df = df[df["course_name"].str.contains(
                    r"Education|Teaching|Pedagogy|Training|Educational|Curriculum|Early Childhood|Primary Education|Secondary Education|Special Education|TESOL",
                    case=False, na=False, regex=True
                )]
            elif "law" in field:
                df = df[df["course_name"].str.contains(
                    r"Law|Legal|Justice|\bLLB\b|\bLLM\b|Jurisprudence|Legal Studies|International Law|Criminal Law|Commercial Law|Corporate Law",
                    case=False, na=False, regex=True
                )]
            elif "media" in field:
                df = df[df["course_name"].str.contains(
                    r"Media|Communication|Journalism|Broadcasting|Digital Media|Mass Communication|Public Relations|Film|Television|Radio|Multimedia",
                    case=False, na=False, regex=True
                )]
            elif "marine" in field:
                df = df[df["course_name"].str.contains(
                    r"Marine|Maritime|Ocean|Naval|Nautical|Shipping|Port|Fisheries|Aquatic|Maritime Engineering|Marine Biology|Naval Architecture|Offshore",
                    case=False, na=False, regex=True
                )]
        
        # Field-based filtering for Diploma
        elif level == "DIPLOMA" and student_vec.get("diploma_field"):
            field = student_vec["diploma_field"].lower()
            
            # First, exclude IT courses globally for non-IT fields to prevent leakage
            if "computing" not in field and "it" not in field:
                df = df[~df["course_name"].str.contains(
                    r"\bIT\b|Information Technology|Computing|Computer Science|Software Engineering|Programming|Data Science|Cyber Security|Network|Systems|Database|Cloud Computing|DevOps|\bAI\b|Artificial Intelligence|Machine Learning|Web Development",
                    case=False, na=False, regex=True
                )]
            
            if "computing" in field or "it" in field:
                df = df[df["course_name"].str.contains(
                    r"Computing|Computer|Software|\bIT\b|Information Technology|Cyber|Data Science|Network|Programming|Web Development|IT Management|Systems|Database|Cloud|DevOps|\bAI\b|Artificial Intelligence|Machine Learning",
                    case=False, na=False, regex=True
                )]
            elif "business" in field:
                df = df[df["course_name"].str.contains(
                    r"Business|\bBBA\b|Entrepreneurship|Commerce|Business Administration|Corporate Strategy|Business Analytics|Supply Chain",
                    case=False, na=False, regex=True
                )]
            elif "engineering" in field:
                df = df[df["course_name"].str.contains(
                    r"Engineering|Technology|Architecture|Construction|Civil|Mechanical|Electrical|Electronic|Chemical|Industrial|Structural|Building|Quantity Survey",
                    case=False, na=False, regex=True
                )]
            elif "health" in field:
                df = df[df["course_name"].str.contains(
                    r"Health|Medicine|Nursing|Pharmacy|Medical|Clinical|Healthcare|Public Health|Biomedical|Physiotherapy|Nutrition|Epidemiology|Health Sciences",
                    case=False, na=False, regex=True
                )]
            elif "arts" in field or "design" in field:
                df = df[df["course_name"].str.contains(
                    r"Arts|Design|Creative|Graphics|Media|Visual|Interior|Fashion|Animation|Illustration|Fine Arts|Digital Arts|\bUX\b|\bUI\b",
                    case=False, na=False, regex=True
                )]
            elif "accounting" in field or "finance" in field:
                df = df[df["course_name"].str.contains(
                    r"Accounting|Finance|Banking|Economics|Financial|Audit|Taxation|ACCA|CIMA|CMA|Investment|Treasury",
                    case=False, na=False, regex=True
                )]
            elif "marketing" in field:
                df = df[df["course_name"].str.contains(
                    r"Marketing|Sales|Digital Marketing|Brand|Advertising|Consumer|Market Research|Social Media Marketing|Content Marketing",
                    case=False, na=False, regex=True
                )]
            elif "management" in field:
                df = df[df["course_name"].str.contains(
                    r"Management|Leadership|Administration|Strategic|Operations|Project Management|Human Resource|\bHRM\b|Organizational|Executive",
                    case=False, na=False, regex=True
                )]
            elif "psychology" in field:
                df = df[df["course_name"].str.contains(
                    r"Psychology|Counseling|Mental Health|Behavioral|Clinical Psychology|Cognitive|Developmental|Social Psychology|Psychotherapy|Psychiatric",
                    case=False, na=False, regex=True
                )]
            elif "education" in field:
                df = df[df["course_name"].str.contains(
                    r"Education|Teaching|Pedagogy|Training|Educational|Curriculum|Early Childhood|Primary Education|Secondary Education|Special Education|TESOL",
                    case=False, na=False, regex=True
                )]
            elif "law" in field:
                df = df[df["course_name"].str.contains(
                    r"Law|Legal|Justice|\bLLB\b|\bLLM\b|Jurisprudence|Legal Studies|International Law|Criminal Law|Commercial Law|Corporate Law",
                    case=False, na=False, regex=True
                )]
            elif "media" in field:
                df = df[df["course_name"].str.contains(
                    r"Media|Communication|Journalism|Broadcasting|Digital Media|Mass Communication|Public Relations|Film|Television|Radio|Multimedia",
                    case=False, na=False, regex=True
                )]
            elif "marine" in field:
                df = df[df["course_name"].str.contains(
                    r"Marine|Maritime|Ocean|Naval|Nautical|Shipping|Port|Fisheries|Aquatic|Maritime Engineering|Marine Biology|Naval Architecture|Offshore",
                    case=False, na=False, regex=True
                )]
        
        # Field-based filtering for Degree (BSc)
        elif level == "BSC" and student_vec.get("degree_field"):
            field = student_vec["degree_field"].lower()
            
            # First, exclude IT courses globally for non-IT fields to prevent leakage
            if "computer" not in field and "computing" not in field and "data" not in field and "cyber" not in field:
                df = df[~df["course_name"].str.contains(
                    r"\bIT\b|Information Technology|Computing|Computer Science|Software Engineering|Software Development|Programming|Data Science|Cyber Security|Network|Systems|Database|Cloud Computing|DevOps|\bAI\b|Artificial Intelligence|Machine Learning|Web Development|Full Stack|Mobile Development",
                    case=False, na=False, regex=True
                )]
            
            if "computer" in field or "computing" in field:
                df = df[df["course_name"].str.contains(
                    r"Computer|Computing|Software|\bIT\b|Information Technology|Cyber|Data Science|Network|Programming|Web Development|Systems|Database|Cloud|DevOps|\bAI\b|Artificial Intelligence|Machine Learning|Full Stack|Mobile|App Development",
                    case=False, na=False, regex=True
                )]
            elif "business" in field:
                df = df[df["course_name"].str.contains(
                    r"Business|\bMBA\b|\bBBA\b|Entrepreneurship|Commerce|Business Administration|Corporate Strategy|Business Analytics|International Business|Business Management|Business Studies",
                    case=False, na=False, regex=True
                )]
            elif "engineering" in field:
                df = df[df["course_name"].str.contains(
                    r"Engineering|Technology|Architecture|Civil|Mechanical|Electrical|Electronic|Chemical|Industrial|Structural|Automotive|Aerospace|Biomedical Engineering|Manufacturing",
                    case=False, na=False, regex=True
                )]
            elif "medicine" in field or "health" in field:
                df = df[df["course_name"].str.contains(
                    r"Medicine|Health|Medical|Clinical|Nursing|Pharmacy|Healthcare|Public Health|Biomedical|Physiotherapy|Nutrition|Health Sciences|Medical Sciences|\bMBBS\b|Surgery|Cardiology|Pathology",
                    case=False, na=False, regex=True
                )]
            elif "psychology" in field:
                df = df[df["course_name"].str.contains(
                    r"Psychology|Counseling|Mental Health|Behavioral|Clinical Psychology|Cognitive|Developmental|Social Psychology|Psychotherapy|Psychiatric|Behavioral Science",
                    case=False, na=False, regex=True
                )]
            elif "accounting" in field or "finance" in field:
                df = df[df["course_name"].str.contains(
                    r"Accounting|Finance|Banking|Financial Management|Audit|Taxation|ACCA|CIMA|CMA|Investment|Treasury|Financial Planning|Corporate Finance|Management Accounting",
                    case=False, na=False, regex=True
                )]
            elif "marketing" in field:
                df = df[df["course_name"].str.contains(
                    r"Marketing|Digital Marketing|Brand|Advertising|Sales|Consumer|Market Research|Social Media Marketing|Content Marketing|Marketing Management|Strategic Marketing|International Marketing",
                    case=False, na=False, regex=True
                )]
            elif "management" in field:
                df = df[df["course_name"].str.contains(
                    r"Management|Leadership|Administration|Strategic|Operations|Project Management|Human Resource|\bHRM\b|Organizational|Executive|Supply Chain|Business Management|General Management",
                    case=False, na=False, regex=True
                )]
            elif "economics" in field:
                df = df[df["course_name"].str.contains(
                    r"Economics|International Trade|Development Economics|Macroeconomics|Microeconomics|Applied Economics|Economic Policy|Political Economy|Business Economics|Financial Economics",
                    case=False, na=False, regex=True
                )]
            elif "law" in field:
                df = df[df["course_name"].str.contains(
                    r"Law|Legal|Justice|\bLLB\b|\bLLM\b|Jurisprudence|Legal Studies|International Law|Criminal Law|Commercial Law|Corporate Law|Constitutional Law|Contract Law",
                    case=False, na=False, regex=True
                )]
            elif "education" in field:
                df = df[df["course_name"].str.contains(
                    r"Education|Teaching|Pedagogy|Training|Educational|Curriculum|Early Childhood|Primary Education|Secondary Education|Special Education|TESOL|Educational Leadership|Teacher Training",
                    case=False, na=False, regex=True
                )]
            elif "arts" in field:
                df = df[df["course_name"].str.contains(
                    r"Arts|Humanities|Literature|History|Philosophy|Creative Writing|English Literature|Sociology|Anthropology|Cultural Studies|Liberal Arts|Fine Arts",
                    case=False, na=False, regex=True
                )]
            elif "data" in field:
                df = df[df["course_name"].str.contains(
                    r"Data|Analytics|Business Intelligence|Statistics|Data Science|Big Data|Data Analytics|Data Engineering|Business Analytics|Predictive Analytics|Data Mining",
                    case=False, na=False, regex=True
                )]
            elif "cyber" in field:
                df = df[df["course_name"].str.contains(
                    r"Cyber|Security|Information Security|Network Security|Cybersecurity|Ethical Hacking|Information Assurance|Digital Forensics|Security Management|Penetration Testing",
                    case=False, na=False, regex=True
                )]
            elif "marine" in field:
                df = df[df["course_name"].str.contains(
                    r"Marine|Maritime|Ocean|Naval|Nautical|Shipping|Port|Fisheries|Aquatic|Maritime Engineering|Marine Biology|Naval Architecture|Offshore|Oceanography|Marine Science",
                    case=False, na=False, regex=True
                )]

    elif level == "POSTGRAD":
        df = df[df["course_name"].str.contains(
            "MSc|Master|MBA|Postgraduate|PhD|Doctor",
            case=False, na=False
        )]
        
        # Field-based filtering for Postgraduate
        if student_vec.get("postgrad_field"):
            field = student_vec["postgrad_field"].lower()
            
            # First, exclude IT courses globally for non-IT fields
            if "computer" not in field and "it" not in field and "data" not in field:
                df = df[~df["course_name"].str.contains(
                    r"\bIT\b|Information Technology|Computing|Computer Science|Software Engineering|Programming|Data Science|Cyber Security|Network|Systems|Database|Cloud|DevOps|\bAI\b|Machine Learning",
                    case=False, na=False, regex=True
                )]
            
            if "computer" in field or "it" in field:
                df = df[df["course_name"].str.contains(
                    r"Computer|Computing|Software|\bIT\b|Information Technology|Cyber|Data Science|Network|\bAI\b|Artificial Intelligence|Machine Learning|Cloud|Systems|Database|Programming",
                    case=False, na=False, regex=True
                )]
            elif "business" in field or "management" in field:
                df = df[df["course_name"].str.contains(
                    r"Business|\bMBA\b|Management|Entrepreneurship|Leadership|Executive|Strategic Management|Business Administration|Operations Management",
                    case=False, na=False, regex=True
                )]
            elif "engineering" in field:
                df = df[df["course_name"].str.contains(
                    r"Engineering|Technology|Civil|Mechanical|Electrical|Industrial|Systems Engineering|Engineering Management",
                    case=False, na=False, regex=True
                )]
            elif "medicine" in field or "health" in field:
                df = df[df["course_name"].str.contains(
                    r"Medicine|Health|Medical|Clinical|Public Health|Nursing|Healthcare Management|Health Sciences|Biomedical|Epidemiology",
                    case=False, na=False, regex=True
                )]
            elif "psychology" in field:
                df = df[df["course_name"].str.contains(
                    r"Psychology|Counseling|Mental Health|Behavioral|Clinical Psychology|Psychotherapy|Organizational Psychology",
                    case=False, na=False, regex=True
                )]
            elif "finance" in field or "economics" in field:
                df = df[df["course_name"].str.contains(
                    r"Finance|Economics|Banking|Accounting|Financial Management|Investment|Financial Economics|Applied Economics",
                    case=False, na=False, regex=True
                )]
            elif "law" in field:
                df = df[df["course_name"].str.contains(
                    r"Law|Legal|\bLLM\b|Justice|International Law|Corporate Law|Commercial Law|Human Rights",
                    case=False, na=False, regex=True
                )]
            elif "education" in field:
                df = df[df["course_name"].str.contains(
                    r"Education|Teaching|Pedagogy|Educational Leadership|Curriculum|Higher Education|TESOL",
                    case=False, na=False, regex=True
                )]
            elif "data" in field:
                df = df[df["course_name"].str.contains(
                    r"Data Science|Data Analytics|\bAI\b|Artificial Intelligence|Machine Learning|Big Data|Business Analytics|Data Engineering",
                    case=False, na=False, regex=True
                )]
            elif "marketing" in field:
                df = df[df["course_name"].str.contains(
                    r"Marketing|Digital Marketing|Advertising|Brand Management|Strategic Marketing|Marketing Management",
                    case=False, na=False, regex=True
                )]
            elif "social" in field:
                df = df[df["course_name"].str.contains(
                    r"Social|Sociology|Political|International Relations|Development Studies|Social Work|Public Policy",
                    case=False, na=False, regex=True
                )]
            elif "marine" in field:
                df = df[df["course_name"].str.contains(
                    r"Marine|Maritime|Ocean|Naval|Nautical|Shipping|Port Management|Fisheries|Aquatic|Maritime Engineering|Marine Biology|Naval Architecture|Offshore|Oceanography|Marine Science|Maritime Law",
                    case=False, na=False, regex=True
                )]

    if df.empty:
        return {
            "level": level,
            "recommendations": []
        }

    # -------------------------
    # Feature engineering
    # -------------------------
    df["requires_al"] = df["eligibility"].apply(
        lambda x: x.get("requires_al", 0) if isinstance(x, dict) else 0
    )

    df["english_required"] = df["eligibility"].apply(
        lambda x: x.get("english_required", 0) if isinstance(x, dict) else 0
    )

    df["math_required"] = df["eligibility"].apply(
        lambda x: x.get("math_required", 0) if isinstance(x, dict) else 0
    )

    feature_cols = ["requires_al", "english_required", "math_required"]
    X = df[feature_cols].fillna(0)

    # -------------------------
    # Student vector
    # -------------------------
    student_df = pd.DataFrame([{
        "requires_al": 1 if student_vec["al_passes"] >= 3 else 0,
        "english_required": 1 if student_vec["english"] else 0,
        "math_required": 1 if student_vec["maths"] else 0
    }])

    # -------------------------
    # Similarity score
    # -------------------------
    similarity_scores = cosine_similarity(X, student_df).flatten()
    df["match_score"] = similarity_scores

    # -------------------------
    # ML eligibility probability
    # -------------------------
    try:
        df["eligibility_score"] = model.predict_proba(X)[:, 1]
    except Exception:
        df["eligibility_score"] = 0.5

    # -------------------------
    # GPA-based scoring boost (for HND, Diploma, BSc, Postgrad)
    # -------------------------
    gpa_boost = 0
    if level in {"HND", "DIPLOMA", "BSC", "POSTGRAD"}:
        gpa = (
            getattr(student, "gpa", None) or 
            student_vec.get("gpa", None)
        )
        if gpa is not None and gpa > 0:
            # Enhanced GPA scoring for BSC: 0-40% based on GPA (0-4 scale)
            # This ensures BSC students with high GPA get better scores
            # Low GPA (2.0) = 20%, Medium GPA (3.0) = 30%, High GPA (4.0) = 40%
            if level == "BSC":
                gpa_boost = (gpa / 4.0) * 0.40
            else:
                # Other levels: 0-35%
                gpa_boost = (gpa / 4.0) * 0.35

    # -------------------------
    # O/L pass-based scoring boost (for O/L level only)
    # -------------------------
    ol_pass_boost = 0
    if level == "OL":
        ol_passes = student_vec.get("ol_passes", 0)
        # Progressive scoring based on O/L passes: 0-30% based on performance
        # 0-3 passes: 0-15%, 4-5 passes: 15-20%, 6-7 passes: 20-25%, 8-9 passes: 25-30%
        if ol_passes >= 8:
            ol_pass_boost = 0.30  # Excellent performance
        elif ol_passes >= 6:
            ol_pass_boost = 0.23  # Good performance
        elif ol_passes >= 4:
            ol_pass_boost = 0.17  # Average performance
        else:
            ol_pass_boost = 0.10  # Basic performance
        
        # Additional bonus for key subjects (English, Maths, Science)
        key_subject_count = sum([
            student_vec.get("english", False),
            student_vec.get("maths", False),
            student_vec.get("science", False)
        ])
        # Add 5% for each key subject passed (up to 15% total)
        ol_pass_boost += (key_subject_count * 0.05)

    # -------------------------
    # A/L pass-based scoring boost (for A/L level only)
    # -------------------------
    al_pass_boost = 0
    if level == "AL":
        al_passes = student_vec.get("al_passes", 0)
        # Professional A/L scoring: Higher weight for A/L passes
        # 3 passes = 40%, 2 passes = 25%, 1 pass = 15%, 0 passes = 5%
        if al_passes >= 3:
            al_pass_boost = 0.40  # Excellent - 3 passes
        elif al_passes == 2:
            al_pass_boost = 0.25  # Good - 2 passes
        elif al_passes == 1:
            al_pass_boost = 0.15  # Fair - 1 pass
        else:
            al_pass_boost = 0.05  # Basic - 0 passes (foundation entry)

    # -------------------------
    # Field matching bonus - Realistic professional scoring
    # -------------------------
    field_match_bonus = 0
    if level in {"AL", "HND", "DIPLOMA", "BSC", "POSTGRAD"}:
        student_field = (
            student_vec.get("stream") or 
            student_vec.get("hnd_field") or 
            student_vec.get("diploma_field") or 
            student_vec.get("degree_field") or
            student_vec.get("postgrad_field")
        )
        
        if student_field:
            # Field-matched courses get moderate boost (15%)
            field_match_bonus = 0.15

    # -------------------------
    # English proficiency bonus - Enhanced for BSC and A/L students
    # -------------------------
    english_bonus = 0
    if student_vec.get("english"):
        if level == "AL":
            english_bonus = 0.10  # 10% bonus for A/L students with English
        elif level == "BSC":
            english_bonus = 0.08  # 8% bonus for BSC students with English (important for postgrad preparation)
        else:
            english_bonus = 0.05  # 5% bonus for other levels

    # -------------------------
    # Institution recognized bonus (for Diploma only)
    # -------------------------
    institution_bonus = 0
    if level == "DIPLOMA":
        if getattr(student, "institution_recognized", False):
            institution_bonus = 0.05  # 5% bonus for recognized institution

    # -------------------------
    # Research experience bonus (for Postgraduate only)
    # -------------------------
    research_bonus = 0
    if level == "POSTGRAD":
        if getattr(student, "research_experience", False):
            research_bonus = 0.10  # 10% bonus for research experience

    # A/L: Professional scoring ensuring 3 passes + English > 75%
    # Others: Balanced to ensure low GPA = 50-65%, medium GPA = 65-75%, high GPA = 80-95%
    # AI: Semantic score provides intelligent matching beyond keywords
    # -------------------------
    
    # Ensure semantic_score exists (for fallback cases)
    if "semantic_score" not in df.columns:
        df["semantic_score"] = 0.5
    
    if level == "OL":
        # O/L specific scoring: base match + eligibility + pass boost + English bonus + AI
        df["final_score"] = (
            0.20 * df["semantic_score"] +    # AI semantic matching (20%)
            0.20 * df["match_score"] +        # Traditional similarity (20%)
            0.20 * df["eligibility_score"] +  # ML model (20%)
            ol_pass_boost +                   # Pass boost (up to 30%)
            english_bonus                     # English bonus (up to 15%)
        )
    elif level == "AL":
        # A/L specific scoring with AI enhancement
        df["final_score"] = (
            0.25 * df["semantic_score"] +     # AI semantic matching (25%)
            0.15 * df["match_score"] +        # Traditional similarity (15%)
            0.10 * df["eligibility_score"] +  # ML model (10%)
            al_pass_boost +                   # Pass boost (up to 40%)
            english_bonus +                   # English bonus (10%)
            field_match_bonus                 # Field match (15%)
        )
    else:
        # Other levels: standard scoring with AI enhancement
        df["final_score"] = (
            0.30 * df["semantic_score"] +     # AI semantic matching (30%)
            0.15 * df["match_score"] +        # Traditional similarity (15%)
            0.15 * df["eligibility_score"] +  # ML model (15%)
            gpa_boost +                       # GPA boost (up to 35%)
            field_match_bonus +               # Field match (15%)
            english_bonus +                   # English bonus (5-8%)
            institution_bonus +               # Institution bonus (5%)
            research_bonus                    # Research bonus (10%)
        )
    
    # Cap final score at 100% (1.0)
    df["final_score"] = df["final_score"].clip(upper=1.0)

    # -------------------------
    # Filter out invalid entries (lecturer names, research titles, etc.)
    # -------------------------
    # Exclude entries that look like person names (Mr., Ms., Dr., Prof., etc.)
    df = df[~df["course_name"].str.contains(
        r"\bMr\b|\bMs\b|\bMrs\b|\bDr\b|\bProf\b|\bProfessor\b",
        case=False, na=False, regex=True
    )]
    
    # Exclude entries that look like research papers or lecturer profiles
    # (typically have very long names with specific details)
    df = df[df["course_name"].str.len() < 150]
    
    # Filter out entries that don't look like proper course names
    # Proper courses usually have keywords like: BSc, BA, MSc, MA, MBA, Diploma, Certificate, etc.
    df = df[df["course_name"].str.contains(
        r"\bBSc\b|\bBA\b|\bBEng\b|\bMSc\b|\bMA\b|\bMBA\b|\bMBBS\b|\bLLB\b|\bLLM\b|Diploma|Certificate|Bachelor|Master|Degree|Course|Program|Programme",
        case=False, na=False, regex=True
    )]
    
    if df.empty:
        return {
            "level": level,
            "recommendations": []
        }

    # -------------------------
    # Return top results with institution info (if available)
    # -------------------------
    # Extract institution name from source_url, handling www subdomain
    def extract_institution(url):
        if not isinstance(url, str) or "." not in url:
            return "Unknown"
        try:
            # Get the domain part (e.g., "www.anc.edu.lk" from "https://www.anc.edu.lk/path")
            domain = url.split("/")[2] if "/" in url else url
            domain_parts = domain.split(".")
            
            # Remove 'www' if it's the first part
            if domain_parts[0].lower() == "www" and len(domain_parts) > 1:
                domain_parts = domain_parts[1:]
            
            # Return the first part (institution name)
            return domain_parts[0] if domain_parts else "Unknown"
        except:
            return "Unknown"
    
    # Always regenerate institution from source_url to ensure consistency
    df["institution"] = df["source_url"].apply(extract_institution)
    
    results = (
        df.sort_values("final_score", ascending=False)
        .head(12)[["course_name", "source_url", "final_score", "institution"]]
        .to_dict(orient="records")
    )

    return {
        "level": level,
        "recommendations": results
    }

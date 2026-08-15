from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = FastAPI(title="AI CareerMate")


# ==============================
# OPENAI
# ==============================

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key) if api_key else None


# ==============================
# CORS
# ==============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================
# HOME
# ==============================

@app.get("/")
def home():
    return {
        "message": "AI CareerMate Backend is Running"
    }


# ==============================
# HEALTH
# ==============================

@app.get("/health")
def health():
    return {
        "status": "OK"
    }


# ==============================
# SKILLS
# ==============================

SKILLS = [
    "Python", "Java", "JavaScript", "HTML", "CSS",
    "React", "SQL", "MySQL", "MongoDB", "C", "C++",
    "Git", "GitHub", "FastAPI", "Django", "Flask",
    "Machine Learning", "Deep Learning", "Data Science",
    "Artificial Intelligence", "AI", "Pandas", "NumPy",
    "TensorFlow", "PyTorch", "Node.js", "Express.js",
    "Angular", "Bootstrap", "PHP", "AWS", "Azure",
    "Docker", "Linux", "Excel", "Power BI", "Tableau"
]


# ==============================
# JOB ROLE DETECTION
# ==============================

def get_job_roles(skills):

    s = [skill.lower() for skill in skills]

    roles = []

    if "python" in s:
        roles.append("Python Developer")

    if "python" in s and (
        "fastapi" in s or
        "django" in s or
        "flask" in s
    ):
        roles.append("Backend Developer")

    if "javascript" in s and "react" in s:
        roles.append("Frontend Developer")

    if (
        "html" in s and
        "css" in s and
        "javascript" in s
    ):
        roles.append("Web Developer")

    if (
        "sql" in s or
        "mysql" in s or
        "mongodb" in s
    ):
        roles.append("Database Developer")

    if (
        "machine learning" in s or
        "data science" in s or
        "tensorflow" in s or
        "pytorch" in s
    ):
        roles.append("Machine Learning / Data Science")

    if (
        "ai" in s or
        "artificial intelligence" in s
    ):
        roles.append("AI Developer")

    if (
        "aws" in s or
        "azure" in s or
        "docker" in s or
        "linux" in s
    ):
        roles.append("Cloud / DevOps Engineer")

    if (
        "excel" in s or
        "power bi" in s or
        "tableau" in s
    ):
        roles.append("Data Analyst")

    if not roles:
        roles.append("Entry-Level Software Developer")

    return roles


# ==============================
# CAREER RECOMMENDATION
# ==============================

def get_career_recommendation(skills):

    s = [skill.lower() for skill in skills]

    recommendations = []

    if "python" in s:
        recommendations.append({
            "role": "Python Developer",
            "reason": "You have Python skills.",
            "learn": [
                "Advanced Python",
                "REST APIs",
                "Git and GitHub",
                "Testing"
            ]
        })

    if (
        "python" in s and
        (
            "fastapi" in s or
            "django" in s or
            "flask" in s
        )
    ):
        recommendations.append({
            "role": "Backend Developer",
            "reason": "Your Python and backend framework skills match backend development.",
            "learn": [
                "REST API Development",
                "Authentication",
                "Docker",
                "Cloud Deployment"
            ]
        })

    if (
        "javascript" in s and
        "react" in s
    ):
        recommendations.append({
            "role": "Frontend Developer",
            "reason": "JavaScript and React are useful frontend development skills.",
            "learn": [
                "Advanced React",
                "TypeScript",
                "API Integration",
                "Responsive Design"
            ]
        })

    if (
        "machine learning" in s or
        "data science" in s or
        "tensorflow" in s or
        "pytorch" in s
    ):
        recommendations.append({
            "role": "Machine Learning Engineer",
            "reason": "Your resume contains machine learning or data science skills.",
            "learn": [
                "Statistics",
                "Scikit-learn",
                "Model Deployment",
                "Deep Learning"
            ]
        })

    if (
        "ai" in s or
        "artificial intelligence" in s
    ):
        recommendations.append({
            "role": "AI Developer",
            "reason": "Your resume contains Artificial Intelligence skills.",
            "learn": [
                "Machine Learning",
                "Deep Learning",
                "LLMs",
                "AI APIs"
            ]
        })

    if (
        "excel" in s or
        "power bi" in s or
        "tableau" in s
    ):
        recommendations.append({
            "role": "Data Analyst",
            "reason": "Your data analysis tools match Data Analyst roles.",
            "learn": [
                "Advanced SQL",
                "Statistics",
                "Power BI",
                "Data Visualization"
            ]
        })

    if not recommendations:
        recommendations.append({
            "role": "Entry-Level Software Developer",
            "reason": "Your resume can be developed toward an entry-level software career.",
            "learn": [
                "Programming Fundamentals",
                "Git and GitHub",
                "SQL",
                "Web Development"
            ]
        })

    return recommendations


# ==============================
# SKILL GAP
# ==============================

def get_skill_gap(skills, job_roles):

    s = [skill.lower() for skill in skills]

    skill_gap = []

    if "Backend Developer" in job_roles:

        required = [
            "Python",
            "SQL",
            "Git",
            "FastAPI",
            "Docker",
            "AWS"
        ]

        for skill in required:
            if skill.lower() not in s:
                skill_gap.append(skill)

    elif "Frontend Developer" in job_roles:

        required = [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Git"
        ]

        for skill in required:
            if skill.lower() not in s:
                skill_gap.append(skill)

    elif "Python Developer" in job_roles:

        required = [
            "Python",
            "SQL",
            "Git",
            "REST API"
        ]

        for skill in required:
            if skill.lower() not in s:
                skill_gap.append(skill)

    elif "AI Developer" in job_roles:

        required = [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "AI"
        ]

        for skill in required:
            if skill.lower() not in s:
                skill_gap.append(skill)

    elif "Data Analyst" in job_roles:

        required = [
            "SQL",
            "Excel",
            "Power BI",
            "Statistics"
        ]

        for skill in required:
            if skill.lower() not in s:
                skill_gap.append(skill)

    return list(dict.fromkeys(skill_gap))


# ==============================
# RESUME SCORE
# ==============================

def calculate_score(text, word_count, skills):

    text_lower = text.lower()

    score = 0

    if word_count >= 300:
        score += 20
    elif word_count >= 150:
        score += 15
    elif word_count >= 80:
        score += 10
    else:
        score += 5

    if len(skills) >= 8:
        score += 20
    elif len(skills) >= 5:
        score += 15
    elif len(skills) >= 3:
        score += 10
    elif len(skills) >= 1:
        score += 5

    sections = {
        "Education": "education" in text_lower,
        "Projects": "project" in text_lower,
        "Experience": (
            "experience" in text_lower or
            "internship" in text_lower
        ),
        "Contact": (
            "email" in text_lower or
            "phone" in text_lower or
            "mobile" in text_lower
        ),
        "Summary": (
            "summary" in text_lower or
            "objective" in text_lower
        )
    }

    for exists in sections.values():
        if exists:
            score += 8

    return min(score, 100), sections


# ==============================
# AI ANALYSIS
# ==============================

def get_ai_analysis(text):

    if not client:
        return {
            "success": False,
            "message": "OpenAI API key is not configured."
        }

    # Limit text so very large resumes do not create unnecessarily
    # large API requests.
    resume_text = text[:15000]

    prompt = f"""
You are an expert AI career advisor.

Analyze the following resume and return ONLY valid JSON.

The JSON must contain exactly these fields:

{{
    "summary": "short professional summary",
    "career_advice": "best career direction based on this resume",
    "improvements": [
        "improvement 1",
        "improvement 2",
        "improvement 3",
        "improvement 4"
    ],
    "skills_to_learn": [
        "skill 1",
        "skill 2",
        "skill 3",
        "skill 4"
    ],
    "interview_questions": [
        "question 1",
        "question 2",
        "question 3",
        "question 4",
        "question 5"
    ]
}}

Do not include markdown.
Do not include ```.

Resume:

{resume_text}
"""

    try:

        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

        ai_text = response.output_text.strip()

        result = json.loads(ai_text)

        return {
            "success": True,
            "data": result
        }

    except Exception as e:

        return {
            "success": False,
            "message": "AI analysis failed.",
            "error": str(e)
        }


# ==============================
# ANALYZE RESUME
# ==============================

@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...)
):

    if not file.filename:

        return {
            "success": False,
            "message": "No file selected.",
            "filename": "",
            "text": ""
        }

    if not file.filename.lower().endswith(".pdf"):

        return {
            "success": False,
            "message": "Please upload a PDF file.",
            "filename": file.filename,
            "text": ""
        }

    contents = await file.read()

    if not contents:

        return {
            "success": False,
            "message": "The uploaded file is empty.",
            "filename": file.filename,
            "text": ""
        }

    temp_file = "temp_resume.pdf"

    try:

        with open(temp_file, "wb") as f:
            f.write(contents)

        reader = PdfReader(temp_file)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"

    except Exception as e:

        return {
            "success": False,
            "message": "Could not read the PDF.",
            "filename": file.filename,
            "text": "",
            "error": str(e)
        }

    word_count = len(text.split())

    text_lower = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill.lower() in text_lower:
            found_skills.append(skill)

    score, sections = calculate_score(
        text,
        word_count,
        found_skills
    )

    job_roles = get_job_roles(
        found_skills
    )

    career_recommendations = get_career_recommendation(
        found_skills
    )

    skill_gap = get_skill_gap(
        found_skills,
        job_roles
    )

    suggestions = []

    if word_count < 150:
        suggestions.append(
            "Add more details about your projects, skills and achievements."
        )

    if len(found_skills) < 3:
        suggestions.append(
            "Add more relevant technical skills."
        )

    if not sections["Education"]:
        suggestions.append(
            "Add a clear Education section."
        )

    if not sections["Projects"]:
        suggestions.append(
            "Add academic or personal projects."
        )

    if not sections["Experience"]:
        suggestions.append(
            "Add internship or work experience if available."
        )

    if not sections["Contact"]:
        suggestions.append(
            "Add your email address and phone number."
        )

    if not sections["Summary"]:
        suggestions.append(
            "Add a professional summary or career objective."
        )

    if not suggestions:
        suggestions.append(
            "Your resume has the important basic sections. Add measurable achievements to make it stronger."
        )

    if score >= 80:

        score_message = (
            "Excellent resume! Keep improving it with measurable achievements."
        )

    elif score >= 60:

        score_message = (
            "Good resume. A few improvements can make it stronger."
        )

    elif score >= 40:

        score_message = (
            "Average resume. Improve your skills, projects and sections."
        )

    else:

        score_message = (
            "Your resume needs improvement. Add more relevant information."
        )

    # ==============================
    # AI
    # ==============================

    ai_analysis = get_ai_analysis(text)

    return {

        "success": True,

        "message":
            "Resume analyzed successfully!",

        "filename":
            file.filename,

        "text":
            text,

        "word_count":
            word_count,

        "skills":
            found_skills,

        "suggestions":
            suggestions,

        "score":
            score,

        "score_message":
            score_message,

        "job_roles":
            job_roles,

        "sections":
            sections,

        "career_recommendations":
            career_recommendations,

        "skill_gap":
            skill_gap,

        "ai_analysis":
            ai_analysis
    }
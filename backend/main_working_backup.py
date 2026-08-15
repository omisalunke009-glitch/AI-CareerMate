
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from io import BytesIO

app = FastAPI(title="AI CareerMate")


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():
    return {
        "message": "AI CareerMate Backend is Running"
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "OK"
    }


# ============================================================
# SKILLS DATABASE
# ============================================================

SKILLS = [
    "Python",
    "Java",
    "JavaScript",
    "HTML",
    "CSS",
    "React",
    "SQL",
    "MySQL",
    "MongoDB",
    "C",
    "C++",
    "Git",
    "GitHub",
    "FastAPI",
    "Django",
    "Flask",
    "Machine Learning",
    "Deep Learning",
    "Data Science",
    "Artificial Intelligence",
    "AI",
    "Pandas",
    "NumPy",
    "TensorFlow",
    "PyTorch",
    "Node.js",
    "Express.js",
    "Angular",
    "Bootstrap",
    "PHP",
    "AWS",
    "Azure",
    "Docker",
    "Linux",
    "Excel",
    "Power BI",
    "Tableau",

    # Healthcare
    "Nursing",
    "Nursing Practices",
    "Patient Care",
    "Emergency Care",
    "ICU",
    "Maternity",
    "Paediatrics",
    "Surgical",
    "Communication",
    "Team Collaboration",
    "Time Management",
    "Problem Solving",
]


# ============================================================
# JOB ROLE DETECTION
# ============================================================

def get_job_roles(skills):

    s = [skill.lower() for skill in skills]

    roles = []

    if "python" in s:
        roles.append("Python Developer")

    if "python" in s and (
        "fastapi" in s
        or "django" in s
        or "flask" in s
    ):
        roles.append("Backend Developer")

    if "javascript" in s and "react" in s:
        roles.append("Frontend Developer")

    if (
        "html" in s
        and "css" in s
        and "javascript" in s
    ):
        roles.append("Web Developer")

    if (
        "sql" in s
        or "mysql" in s
        or "mongodb" in s
    ):
        roles.append("Database Developer")

    if (
        "machine learning" in s
        or "data science" in s
        or "tensorflow" in s
        or "pytorch" in s
    ):
        roles.append("Machine Learning / Data Science")

    if (
        "ai" in s
        or "artificial intelligence" in s
    ):
        roles.append("AI Developer")

    if (
        "aws" in s
        or "azure" in s
        or "docker" in s
        or "linux" in s
    ):
        roles.append("Cloud / DevOps Engineer")

    if (
        "excel" in s
        or "power bi" in s
        or "tableau" in s
    ):
        roles.append("Data Analyst")

    # Healthcare

    if (
        "nursing" in s
        or "nursing practices" in s
        or "patient care" in s
        or "icu" in s
        or "emergency care" in s
    ):
        roles.append("Nurse / Healthcare Professional")

    if (
        "icu" in s
        or "emergency care" in s
    ):
        roles.append("ICU / Emergency Care Nurse")

    if (
        "maternity" in s
        or "paediatrics" in s
        or "surgical" in s
    ):
        roles.append("Clinical Nurse")

    if not roles:
        roles.append("Entry-Level Professional")

    return list(dict.fromkeys(roles))


# ============================================================
# CAREER RECOMMENDATIONS
# ============================================================

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
        "python" in s
        and (
            "fastapi" in s
            or "django" in s
            or "flask" in s
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
        "javascript" in s
        and "react" in s
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
        "machine learning" in s
        or "data science" in s
        or "tensorflow" in s
        or "pytorch" in s
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
        "ai" in s
        or "artificial intelligence" in s
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
        "excel" in s
        or "power bi" in s
        or "tableau" in s
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

    # Healthcare

    if (
        "nursing" in s
        or "nursing practices" in s
        or "patient care" in s
    ):
        recommendations.append({
            "role": "Nurse / Healthcare Professional",
            "reason": "Your resume contains nursing and patient-care experience.",
            "learn": [
                "Advanced Patient Care",
                "Clinical Documentation",
                "Emergency Care",
                "Patient Safety"
            ]
        })

    if (
        "icu" in s
        or "emergency care" in s
    ):
        recommendations.append({
            "role": "ICU / Emergency Care Nurse",
            "reason": "Your resume shows ICU or emergency-care related skills.",
            "learn": [
                "Critical Care Nursing",
                "Emergency Nursing",
                "Patient Monitoring",
                "Advanced Life Support"
            ]
        })

    if (
        "maternity" in s
        or "paediatrics" in s
        or "surgical" in s
    ):
        recommendations.append({
            "role": "Clinical Nurse",
            "reason": "Your clinical training includes multiple healthcare departments.",
            "learn": [
                "Clinical Nursing",
                "Patient Assessment",
                "Infection Control",
                "Clinical Documentation"
            ]
        })

    if not recommendations:
        recommendations.append({
            "role": "Entry-Level Professional",
            "reason": "Your resume can be developed toward a suitable entry-level career.",
            "learn": [
                "Communication Skills",
                "Professional Skills",
                "Computer Skills",
                "Industry Knowledge"
            ]
        })

    return recommendations


# ============================================================
# SKILL GAP
# ============================================================

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

    elif (
        "Nurse / Healthcare Professional" in job_roles
        or "Clinical Nurse" in job_roles
    ):

        required = [
            "Nursing",
            "Patient Care",
            "Communication",
            "Problem Solving",
            "Team Collaboration"
        ]

        for skill in required:
            if skill.lower() not in s:
                skill_gap.append(skill)

    elif "ICU / Emergency Care Nurse" in job_roles:

        required = [
            "Nursing",
            "ICU",
            "Emergency Care",
            "Patient Care",
            "Problem Solving"
        ]

        for skill in required:
            if skill.lower() not in s:
                skill_gap.append(skill)

    return list(dict.fromkeys(skill_gap))


# ============================================================
# RESUME SCORE
# ============================================================

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
        "Education": (
            "education" in text_lower
            or "academic qualification" in text_lower
            or "professional qualification" in text_lower
        ),

        "Projects": (
            "project" in text_lower
        ),

        "Experience": (
            "experience" in text_lower
            or "internship" in text_lower
            or "clinical training" in text_lower
        ),

        "Contact": (
            "email" in text_lower
            or "phone" in text_lower
            or "mobile" in text_lower
        ),

        "Summary": (
            "summary" in text_lower
            or "objective" in text_lower
            or "career objective" in text_lower
        )
    }

    for exists in sections.values():
        if exists:
            score += 8

    return min(score, 100), sections


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_pdf_text(contents):

    reader = PdfReader(BytesIO(contents))

    text = ""

    for page in reader.pages:

        page_text = page.extract_text() or ""

        text += page_text + "\n"

    return text


# ============================================================
# ANALYZE RESUME
# ============================================================

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

    try:

        text = extract_pdf_text(contents)

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
            "Add more relevant professional or technical skills."
        )

    if not sections["Education"]:

        suggestions.append(
            "Add a clear Education section."
        )

    if not sections["Projects"]:

        suggestions.append(
            "Add academic or personal projects if relevant to your career."
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

    return {

        "success": True,

        "message": "Resume analyzed successfully!",

        "filename": file.filename,

        "text": text,

        "word_count": word_count,

        "skills": found_skills,

        "suggestions": suggestions,

        "score": score,

        "score_message": score_message,

        "job_roles": job_roles,

        "sections": sections,

        "career_recommendations": career_recommendations,

        "skill_gap": skill_gap
    }


# ============================================================
# JOB DATABASE
# ============================================================

JOBS = [

    {
        "title": "Python Developer",
        "company": "AI CareerMate Jobs",
        "location": "Remote",
        "skills": [
            "Python",
            "SQL",
            "Git",
            "REST API"
        ]
    },

    {
        "title": "Backend Developer",
        "company": "AI CareerMate Jobs",
        "location": "Remote",
        "skills": [
            "Python",
            "FastAPI",
            "SQL",
            "Git",
            "Docker"
        ]
    },

    {
        "title": "Frontend Developer",
        "company": "AI CareerMate Jobs",
        "location": "Remote",
        "skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Git"
        ]
    },

    {
        "title": "Full Stack Developer",
        "company": "AI CareerMate Jobs",
        "location": "Remote",
        "skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Node.js",
            "SQL"
        ]
    },

    {
        "title": "Java Developer",
        "company": "AI CareerMate Jobs",
        "location": "Remote",
        "skills": [
            "Java",
            "Spring Boot",
            "SQL",
            "Git"
        ]
    },

    {
        "title": "Web Developer",
        "company": "AI CareerMate Jobs",
        "location": "Remote",
        "skills": [
            "HTML",
            "CSS",
            "JavaScript"
        ]
    },

    {
        "title": "Data Analyst",
        "company": "AI CareerMate Jobs",
        "location": "Remote",
        "skills": [
            "Python",
            "SQL",
            "Excel",
            "Power BI"
        ]
    },

    {
        "title": "Data Scientist",
        "company": "AI CareerMate Jobs",
        "location": "Remote",
        "skills": [
            "Python",
            "SQL",
            "Pandas",
            "NumPy",
            "Machine Learning"
        ]
    },

    {
        "title": "Machine Learning Engineer",
        "company": "AI CareerMate Jobs",
        "location": "Remote",
        "skills": [
            "Python",
            "Machine Learning",
            "TensorFlow",
            "PyTorch"
        ]
    },

    {
        "title": "AI Developer",
        "company": "AI CareerMate Jobs",
        "location": "Remote",
        "skills": [
            "Python",
            "Artificial Intelligence",
            "Machine Learning",
            "Deep Learning"
        ]
    },

    {
        "title": "Cloud Engineer",
        "company": "AI CareerMate Jobs",
        "location": "Remote",
        "skills": [
            "AWS",
            "Linux",
            "Docker",
            "Git"
        ]
    },

    {
        "title": "DevOps Engineer",
        "company": "AI CareerMate Jobs",
        "location": "Remote",
        "skills": [
            "Linux",
            "Docker",
            "Git",
            "AWS"
        ]
    },

    {
        "title": "Database Developer",
        "company": "AI CareerMate Jobs",
        "location": "Remote",
        "skills": [
            "SQL",
            "MySQL",
            "MongoDB"
        ]
    },

    {
        "title": "Nurse / Healthcare Professional",
        "company": "AI CareerMate Healthcare",
        "location": "India",
        "skills": [
            "Nursing",
            "Patient Care",
            "Communication",
            "Problem Solving"
        ]
    },

    {
        "title": "Clinical Nurse",
        "company": "AI CareerMate Healthcare",
        "location": "India",
        "skills": [
            "Nursing",
            "Patient Care",
            "Clinical Training",
            "Infection Control"
        ]
    },

    {
        "title": "ICU / Emergency Care Nurse",
        "company": "AI CareerMate Healthcare",
        "location": "India",
        "skills": [
            "Nursing",
            "ICU",
            "Emergency Care",
            "Patient Care"
        ]
    },

    {
        "title": "Maternity Nurse",
        "company": "AI CareerMate Healthcare",
        "location": "India",
        "skills": [
            "Nursing",
            "Maternity",
            "Patient Care"
        ]
    },

    {
        "title": "Paediatric Nurse",
        "company": "AI CareerMate Healthcare",
        "location": "India",
        "skills": [
            "Nursing",
            "Paediatrics",
            "Patient Care"
        ]
    }

]


# ============================================================
# JOB MATCH CALCULATION
# ============================================================

def calculate_job_match(
    user_skills,
    required_skills
):

    user_skills_lower = [
        skill.lower()
        for skill in user_skills
    ]

    matched = []

    missing = []

    for skill in required_skills:

        if skill.lower() in user_skills_lower:

            matched.append(skill)

        else:

            missing.append(skill)

    if required_skills:

        percentage = round(
            len(matched)
            / len(required_skills)
            * 100
        )

    else:

        percentage = 0

    return percentage, matched, missing


# ============================================================
# JOB MATCH API
# ============================================================

@app.post("/job-match")
async def job_match(
    file: UploadFile = File(...)
):

    if not file.filename:

        return {
            "success": False,
            "message": "No file selected."
        }

    if not file.filename.lower().endswith(".pdf"):

        return {
            "success": False,
            "message": "Please upload a PDF file."
        }

    contents = await file.read()

    if not contents:

        return {
            "success": False,
            "message": "The uploaded file is empty."
        }

    try:

        text = extract_pdf_text(contents)

    except Exception as e:

        return {
            "success": False,
            "message": "Could not read the PDF.",
            "error": str(e)
        }

    text_lower = text.lower()

    user_skills = []

    for skill in SKILLS:

        if skill.lower() in text_lower:

            user_skills.append(skill)

    results = []

    for job in JOBS:

        percentage, matched, missing = calculate_job_match(
            user_skills,
            job["skills"]
        )

        results.append({

            "title": job["title"],

            "company": job["company"],

            "location": job["location"],

            "match_percentage": percentage,

            "matched_skills": matched,

            "missing_skills": missing

        })

    results.sort(
        key=lambda x: x["match_percentage"],
        reverse=True
    )

    return {

        "success": True,

        "message":
            "Job matching completed successfully!",

        "jobs":
            results

    }


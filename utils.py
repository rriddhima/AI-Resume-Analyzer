from pdfminer.high_level import extract_text
import re
import nltk

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Download NLTK stopwords
nltk.download("stopwords", quiet=True)


# --------------------------------------------------
# 📄 EXTRACT TEXT FROM PDF
# --------------------------------------------------

def extract_resume_text(file_path):
    try:
        return extract_text(file_path)

    except Exception as e:
        return f"Error extracting text: {e}"


# --------------------------------------------------
# 🧹 CLEAN TEXT
# --------------------------------------------------

def clean_text(text):

    # Convert text to lowercase
    text = text.lower()

    # Keep useful characters used in technical skills
    # Examples: c++, react.js, ci/cd, scikit-learn
    text = re.sub(
        r"[^a-zA-Z0-9\s\+\#\./-]",
        " ",
        text
    )

    # Split text into words
    words = text.split()

    # Remove English stopwords
    words = [
        word
        for word in words
        if word not in stopwords.words("english")
        and len(word) > 2
    ]

    return " ".join(words)


# --------------------------------------------------
# 🛠️ SKILL DATABASE
# --------------------------------------------------

SKILLS_DB = {

    "programming": [
        "python",
        "java",
        "javascript",
        "sql",
        "c++",
        "c#"
    ],

    "backend": [
        "spring boot",
        "spring mvc",
        "spring security",
        "hibernate",
        "jpa",
        "flask",
        "rest api",
        "restful api"
    ],

    "frontend": [
        "react",
        "react.js",
        "redux",
        "html",
        "html5",
        "css",
        "css3",
        "bootstrap",
        "tailwind css"
    ],

    "database": [
        "mysql",
        "postgresql",
        "mongodb",
        "redis"
    ],

    "cloud_devops": [
        "aws",
        "ec2",
        "s3",
        "rds",
        "docker",
        "jenkins",
        "git",
        "github",
        "maven",
        "ci/cd"
    ],

    "testing": [
        "junit",
        "mockito"
    ],

    "documentation": [
        "swagger",
        "openapi"
    ],

    "ai_ml": [
        "machine learning",
        "deep learning",
        "nlp",
        "tensorflow",
        "scikit-learn",
        "openai api"
    ]
}


# --------------------------------------------------
# 🔍 EXTRACT SKILLS
# --------------------------------------------------

def extract_skills(text):

    found = set()

    # Convert text to lowercase
    text = text.lower()

    for category in SKILLS_DB:

        for skill in SKILLS_DB[category]:

            # Create regex pattern for exact skill matching
            pattern = (
                r"(?<!\w)"
                + re.escape(skill.lower())
                + r"(?!\w)"
            )

            if re.search(pattern, text):

                found.add(skill)

    return list(found)


# --------------------------------------------------
# 🤖 MATCH ONE RESUME AGAINST MULTIPLE JOBS
# --------------------------------------------------

def match_resume_to_jobs(
    resume_text,
    job_descriptions
):

    corpus = [resume_text] + job_descriptions

    tfidf = TfidfVectorizer(
        ngram_range=(1, 2),
        stop_words="english"
    )

    vectors = tfidf.fit_transform(corpus)

    scores = cosine_similarity(
        vectors[0:1],
        vectors[1:]
    )[0]

    return scores


# --------------------------------------------------
# 📊 TF-IDF MATCH SCORING
# --------------------------------------------------

def compute_tfidf_scores(
    job_text,
    resume_texts
):

    # Return empty list if no resumes exist
    if not resume_texts:
        return []

    # Combine JD and all resumes
    corpus = [job_text] + resume_texts

    # Create TF-IDF vectors
    tfidf = TfidfVectorizer(
        ngram_range=(1, 2),
        stop_words="english"
    )

    vectors = tfidf.fit_transform(corpus)

    # Calculate cosine similarity
    scores = cosine_similarity(
        vectors[0:1],
        vectors[1:]
    )[0]

    # Convert NumPy values to Python floats
    return [
        float(score)
        for score in scores
    ]


# --------------------------------------------------
# 🎯 KEYWORD RECALL
# --------------------------------------------------

def keyword_recall(
    resume_skills,
    job_skills
):

    # Convert to sets
    resume_set = set(resume_skills)
    job_set = set(job_skills)

    # Avoid division by zero
    if not job_set:
        return 0.0

    # Calculate how many JD skills
    # are present in the resume
    matched_skills = (
        resume_set
        &
        job_set
    )

    recall = (
        len(matched_skills)
        /
        len(job_set)
    )

    return recall
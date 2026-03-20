from pdfminer.high_level import extract_text
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords', quiet=True)


# 🔹 Extract text from PDF
def extract_resume_text(file_path):
    try:
        return extract_text(file_path)
    except Exception as e:
        return f"Error extracting text: {e}"


# 🔹 Clean text
def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = text.lower()
    words = text.split()
    words = [
        w for w in words
        if w not in stopwords.words('english') and len(w) > 2
    ]
    return " ".join(words)


# 🔹 Skill database
SKILLS_DB = {
    "programming": ["python", "java", "c", "c++", "javascript"],
    "web": ["html", "css", "react", "node", "express"],
    "database": ["sql", "mysql", "mongodb", "postgresql"],
    "ai_ml": ["machine learning", "deep learning", "nlp", "tensorflow", "scikit learn", "data science"],
    "tools": ["git", "docker", "aws"]
}


# 🔹 Extract skills
def extract_skills(text):
    found = set()
    for category in SKILLS_DB:
        for skill in SKILLS_DB[category]:
            if skill in text:
                found.add(skill)
    return list(found)


# 🔹 Match resume with job (ML)
def match_resume_to_jobs(resume_text, job_descriptions):
    corpus = [resume_text] + job_descriptions
    tfidf = TfidfVectorizer()
    vectors = tfidf.fit_transform(corpus)
    scores = cosine_similarity(vectors[0:1], vectors[1:])
    return scores[0]
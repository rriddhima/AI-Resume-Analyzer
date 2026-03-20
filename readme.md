# 🚀 AI Resume Analyzer

> Transform your resume into a job-ready profile using intelligent skill matching and analysis.

---

## 🌟 Overview

AI Resume Analyzer is a web-based application that evaluates resumes against job descriptions to determine compatibility, highlight skill gaps, and provide actionable insights.

It simulates how recruiters and ATS (Applicant Tracking Systems) assess candidates — helping users understand where they stand and how to improve.

---

## ✨ Key Features

* 📄 **Resume Parsing**
  Extracts text from PDF resumes efficiently

* 🧠 **Skill Extraction (NLP-based)**
  Identifies relevant technical skills from resume content

* 📊 **Match Score Calculation**
  Compares resume with job description using similarity techniques

* ⚠️ **Skill Gap Detection**
  Highlights missing skills required for the role

* 🎯 **User-Friendly Interface**
  Clean, minimal, and intuitive Streamlit UI

---

## 🧪 How It Works

1. Upload your resume (PDF)
2. Enter a job description
3. The system:

   * Cleans and processes text
   * Extracts relevant skills
   * Compares resume vs job requirements
4. Outputs:

   * Match score (%)
   * Matched skills
   * Missing skills

---

## 🛠️ Tech Stack

| Category      | Tools Used                |
| ------------- | ------------------------- |
| Language      | Python                    |
| Frontend      | Streamlit                 |
| NLP           | NLTK                      |
| ML Techniques | TF-IDF, Cosine Similarity |
| PDF Parsing   | pdfminer                  |

---

## 📸 Application Preview

<img width="1352" height="774" alt="image" src="https://github.com/user-attachments/assets/d42d51af-2b9e-4314-a9fb-95bbc48b3ae5" />

---

## 🌐 Live Demo

🔗 https://ai-resume-analyzer-rr.streamlit.app/

---

## 📂 Project Structure

```
AI-Resume-Analyzer/
│
├── app.py               # Main Streamlit app
├── utils.py             # Core logic (NLP + matching)
├── requirements.txt     # Dependencies
├── README.md            # Documentation
```

---

## 🚀 Installation & Setup

```bash
git clone https://github.com/rriddhima/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
pip install -r requirements.txt
streamlit run app.py
```

---

## 📌 Use Cases

* Students preparing for internships
* Job seekers optimizing resumes
* Quick resume-job compatibility checks
* Understanding skill gaps before applying

---

## ⚡ Future Enhancements

* Multi-job comparison
* Resume improvement suggestions
* AI-powered recommendations
* ATS optimization scoring

---

## 👩‍💻 Author

**Riddhima Prasad**

---

## 💡 Inspiration

Built to simplify job preparation by bridging the gap between resumes and real-world job expectations.

---

⭐ If you found this useful, consider starring the repository!

# 🚀 AI Resume Analyzer

An AI-powered resume screening application that analyzes and ranks candidates against a Job Description using **NLP, TF-IDF similarity, and keyword-based skill matching**.

## 📌 Features

- Upload one or multiple resume PDFs
- Paste a Job Description
- Extract text from uploaded resumes
- Extract technical skills from resumes and the Job Description
- Rank candidates based on their job match score
- View matched and missing skills
- Identify common skill gaps across candidates
- View detailed candidate analysis
- Interactive ranking and analytics dashboard

## 🛠️ Technologies Used

- Python
- Streamlit
- NLTK
- Scikit-learn
- Pandas
- Altair
- pdfminer.six

---

# ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/rriddhima/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

The application will open automatically at:

```text
http://localhost:8501
```

NLTK stopwords are downloaded automatically on the first run.

---

# 💻 How to Use

### Step 1: Paste a Job Description

Enter the Job Description in the provided text area.

### Step 2: Upload Resume PDFs

Upload one or multiple resume PDFs.

### Step 3: View Results

The application provides three main sections:

## 🏆 Ranking Dashboard

Candidates are ranked based on their **TF-IDF Job Match Score**.

The dashboard helps compare candidates based on how closely their resume content matches the Job Description.

---

## 🔍 Candidate Detail

Select an individual candidate to view:

- TF-IDF match score
- Keyword recall
- Matched skills
- Missing skills
- Skill gap analysis

---

## 📈 Gap Analytics

Analyze skill gaps across all candidates.

The dashboard shows:

- Common missing skills
- Skills missing across candidates
- Candidate score distribution

---

# 🧠 How It Works

### 1. PDF Text Extraction

Resume text is extracted from uploaded PDF files using **pdfminer.six**.

### 2. Text Cleaning

The extracted text is:

- Converted to lowercase
- Cleaned using regular expressions
- Processed by removing English stopwords using NLTK

### 3. Skill Extraction

The system uses a keyword-based skill database to identify technical skills.

Skills are grouped into categories such as:

- Programming
- Backend Development
- Frontend Development
- Databases
- Cloud & DevOps
- Testing
- Documentation
- AI & Machine Learning

### 4. TF-IDF Matching

A TF-IDF vector space is created using:

- The Job Description
- All uploaded resumes

Cosine similarity is then calculated between the Job Description and each resume.

This produces the **TF-IDF Job Match Score** used to rank candidates.

### 5. Keyword Recall

The system compares the skills extracted from the resume with the skills required in the Job Description.

```text
Keyword Recall = Matched JD Skills / Total JD Skills
```

This helps identify how many of the required skills are covered by a candidate.

---

# 📂 Project Structure

```text
AI-Resume-Analyzer/
│
├── app.py
├── utils.py
├── requirements.txt
├── readme.md
├── .gitignore
│
└── sample_resume/
    └── sample.pdf
```

---

# 🔮 Future Improvements

- Support for DOCX resumes
- Larger and more dynamic skill database
- Experience-based candidate scoring
- Education and certification analysis
- AI-based semantic matching using embeddings
- Resume improvement recommendations
- Export candidate analysis reports

---

## 👩‍💻 Author

**Riddhima**

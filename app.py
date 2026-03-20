import streamlit as st
from utils import extract_resume_text, clean_text, extract_skills

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

# 🎨 LIGHT CLEAN UI
st.markdown("""
<style>

/* Background */
[data-testid="stAppViewContainer"] {
    background-color: #f8fafc;
}

/* Layout */
.block-container {
    padding-top: 2rem;
    max-width: 850px;
}

/* Title */
.title {
    font-size: 42px;
    font-weight: 700;
    color: #0f172a;
}

/* Subtitle */
.subtitle {
    color: #64748b;
    margin-bottom: 20px;
}

/* Card */
.card {
    background: white;
    padding: 22px;
    border-radius: 14px;
    box-shadow: 0px 4px 16px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

/* Skill tags */
.skill {
    display: inline-block;
    padding: 6px 12px;
    margin: 6px 6px 0 0;
    border-radius: 999px;
    background: #e0f2fe;
    color: #0369a1;
    font-size: 13px;
    font-weight: 500;
}

/* Missing skills */
.missing {
    background: #fee2e2;
    color: #991b1b;
}

/* Score */
.score {
    font-size: 48px;
    font-weight: 700;
    color: #0f172a;
}

/* Section titles */
.section-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# 🚀 HEADER
st.markdown("<div class='title'>🚀 AI Resume Analyzer</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Match your resume with job descriptions</div>", unsafe_allow_html=True)
st.divider()

# 📄 INPUT SECTION
st.markdown("<div class='card'>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description")

st.markdown("</div>", unsafe_allow_html=True)

# spacing
st.markdown("<br>", unsafe_allow_html=True)

# 🚀 MAIN LOGIC
if uploaded_file and job_description:

    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    text = extract_resume_text("temp.pdf")
    cleaned = clean_text(text)

    resume_skills = extract_skills(cleaned)

    job_cleaned = clean_text(job_description)
    job_skills = extract_skills(job_cleaned)

    resume_set = set(resume_skills)
    job_set = set(job_skills)

    common = resume_set & job_set
    missing = job_set - resume_set

    match_score = len(common) / len(job_set) if job_set else 0

    # 📊 SCORE SECTION
    st.markdown("### 📊 Match Score")

    colA, colB = st.columns([1, 2])

    with colA:
        st.markdown(f"<div class='score'>{int(match_score*100)}%</div>", unsafe_allow_html=True)

    with colB:
        st.progress(match_score)

        if match_score > 0.7:
            st.success("Strong match")
        elif match_score > 0.4:
            st.warning("Moderate match")
        else:
            st.error("Low match")

    st.divider()

    # 🧠 SKILLS SECTION
    col1, col2 = st.columns(2)

    # ✅ MATCHED
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>✅ Matched Skills</div>", unsafe_allow_html=True)

        if common:
            for skill in common:
                st.markdown(f"<span class='skill'>{skill}</span>", unsafe_allow_html=True)
        else:
            st.write("No matches")

        st.markdown("</div>", unsafe_allow_html=True)

    # ❌ MISSING
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>❌ Missing Skills</div>", unsafe_allow_html=True)

        if missing:
            for skill in missing:
                st.markdown(f"<span class='skill missing'>{skill}</span>", unsafe_allow_html=True)
        else:
            st.success("No gaps")

        st.markdown("</div>", unsafe_allow_html=True)
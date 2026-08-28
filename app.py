import os
import tempfile

import pandas as pd
import altair as alt
import streamlit as st

from utils import (
    extract_resume_text,
    clean_text,
    extract_skills,
    compute_tfidf_scores,
    keyword_recall,
)

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

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
    max-width: 1100px;
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

/* Rank badge */
.rank-badge {
    display: inline-block;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #0f172a;
    color: white;
    text-align: center;
    line-height: 28px;
    font-weight: 700;
    margin-right: 10px;
}

</style>
""", unsafe_allow_html=True)


# 🚀 HEADER
st.markdown(
    "<div class='title'>🚀 AI Resume Analyzer</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Rank candidates against a job description using NLP, TF-IDF, and skill matching</div>",
    unsafe_allow_html=True,
)

st.divider()


# 📄 INPUT SECTION
st.markdown("<div class='card'>", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Upload Resumes (PDF) — supports 10+ resumes at once",
    type=["pdf"],
    accept_multiple_files=True,
)

job_description = st.text_area(
    "Paste Job Description",
    height=160
)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def process_resume(file_bytes, file_name):
    """Extract + clean text and pull out skills for a single resume."""

    with tempfile.NamedTemporaryFile(
        suffix=".pdf",
        delete=False
    ) as tmp:

        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        raw_text = extract_resume_text(tmp_path)

    finally:
        os.remove(tmp_path)

    cleaned = clean_text(raw_text)
    skills = extract_skills(cleaned)

    return cleaned, skills


# 🚀 MAIN LOGIC
if uploaded_files and job_description:

    # Clean Job Description
    job_cleaned = clean_text(job_description)

    # Extract skills from Job Description
    job_skills = set(extract_skills(job_cleaned))

    # Store candidate information
    candidates = []
    resume_cleaned_texts = []


    # 🔹 PROCESS RESUMES
    with st.spinner(
        f"Analyzing {len(uploaded_files)} resume(s)..."
    ):

        for f in uploaded_files:

            cleaned, skills = process_resume(
                f.getvalue(),
                f.name
            )

            resume_cleaned_texts.append(cleaned)

            candidates.append({
                "file_name": f.name,
                "cleaned_text": cleaned,
                "skills": set(skills),
            })


        # 🔹 TF-IDF similarity between JD and resumes
        tfidf_scores = compute_tfidf_scores(
            job_cleaned,
            resume_cleaned_texts
        )


    # 🔹 CALCULATE HYBRID MATCH SCORE
    for candidate, score in zip(candidates, tfidf_scores):

        # Common and missing skills
        common = candidate["skills"] & job_skills
        missing = job_skills - candidate["skills"]


        # Keyword Recall Score
        recall_score = keyword_recall(
            candidate["skills"],
            job_skills
        )


        # Hybrid Score
        # 30% TF-IDF similarity
        # 70% Skill / Keyword Recall

        hybrid_score = (
            0.30 * score
            +
            0.70 * recall_score
        )


        # Store scores
        candidate["tfidf_score"] = score

        candidate["match_score"] = hybrid_score

        candidate["common_skills"] = common

        candidate["missing_skills"] = missing

        candidate["recall"] = recall_score


    # 🔹 SORT CANDIDATES BY MATCH SCORE
    ranked = sorted(
        candidates,
        key=lambda c: c["match_score"],
        reverse=True
    )


    # 📊 SUMMARY METRICS

    avg_score = (
        sum(c["match_score"] for c in ranked)
        / len(ranked)
    )

    avg_recall = (
        sum(c["recall"] for c in ranked)
        / len(ranked)
    )


    m1, m2, m3 = st.columns(3)

    m1.metric(
        "Candidates Analyzed",
        len(ranked)
    )

    m2.metric(
        "Avg. Overall Match",
        f"{avg_score * 100:.0f}%"
    )

    m3.metric(
        "Avg. Keyword Recall",
        f"{avg_recall * 100:.0f}%"
    )


    st.divider()


    # 📑 TABS

    tab_rank, tab_detail, tab_analytics = st.tabs(
        [
            "🏆 Ranking Dashboard",
            "🔍 Candidate Detail",
            "📈 Gap Analytics"
        ]
    )


    # ---------------- RANKING TAB ----------------

    with tab_rank:

        st.markdown(
            "<div class='section-title'>Candidates ranked by overall JD match</div>",
            unsafe_allow_html=True
        )


        rank_df = pd.DataFrame([

            {
                "Rank": i + 1,

                "Candidate": c["file_name"],

                "Match Score": round(
                    c["match_score"] * 100,
                    1
                ),

                "TF-IDF Score": round(
                    c["tfidf_score"] * 100,
                    1
                ),

                "Keyword Recall": round(
                    c["recall"] * 100,
                    1
                ),

                "Skills Matched": len(
                    c["common_skills"]
                ),

                "Skills Missing": len(
                    c["missing_skills"]
                ),
            }

            for i, c in enumerate(ranked)

        ])


        chart = alt.Chart(rank_df).mark_bar(
            color="#0369a1",
            cornerRadiusEnd=4
        ).encode(

            x=alt.X(
                "Match Score:Q",
                title="Overall Match Score (%)",
                scale=alt.Scale(domain=[0, 100])
            ),

            y=alt.Y(
                "Candidate:N",
                sort="-x",
                title=None
            ),

            tooltip=[
                "Candidate",
                "Match Score",
                "TF-IDF Score",
                "Keyword Recall",
                "Skills Matched",
                "Skills Missing"
            ],

        ).properties(
            height=max(180, 32 * len(rank_df))
        )


        st.altair_chart(
            chart,
            use_container_width=True
        )

        st.dataframe(
            rank_df,
            use_container_width=True,
            hide_index=True
        )


    # ---------------- CANDIDATE DETAIL TAB ----------------

    with tab_detail:

        names = [
            c["file_name"]
            for c in ranked
        ]

        selected_name = st.selectbox(
            "Select a candidate",
            names
        )

        candidate = next(
            c for c in ranked
            if c["file_name"] == selected_name
        )


        colA, colB = st.columns([1, 2])


        # LEFT SIDE — SCORE

        with colA:

            st.markdown(
                f"<div class='score'>{int(candidate['match_score'] * 100)}%</div>",
                unsafe_allow_html=True
            )

            st.caption(
                "Overall JD Match Score"
            )


        # RIGHT SIDE — PROGRESS

        with colB:

            st.progress(
                candidate["match_score"]
            )


            if candidate["match_score"] > 0.7:

                st.success("Strong match")

            elif candidate["match_score"] > 0.4:

                st.warning("Moderate match")

            else:

                st.error("Low match")


            st.caption(
                f"TF-IDF similarity: "
                f"{candidate['tfidf_score'] * 100:.0f}%"
            )

            st.caption(
                f"Keyword recall: "
                f"{candidate['recall'] * 100:.0f}%"
            )


        st.divider()


        # ---------------- SKILLS ----------------

        col1, col2 = st.columns(2)


        # MATCHED SKILLS

        with col1:

            st.markdown(
                "<div class='card'>",
                unsafe_allow_html=True
            )

            st.markdown(
                "<div class='section-title'>✅ Matched Skills</div>",
                unsafe_allow_html=True
            )


            if candidate["common_skills"]:

                for skill in sorted(
                    candidate["common_skills"]
                ):

                    st.markdown(
                        f"<span class='skill'>{skill}</span>",
                        unsafe_allow_html=True
                    )

            else:

                st.write("No matches")


            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


        # MISSING SKILLS

        with col2:

            st.markdown(
                "<div class='card'>",
                unsafe_allow_html=True
            )

            st.markdown(
                "<div class='section-title'>❌ Missing Skills</div>",
                unsafe_allow_html=True
            )


            if candidate["missing_skills"]:

                for skill in sorted(
                    candidate["missing_skills"]
                ):

                    st.markdown(
                        f"<span class='skill missing'>{skill}</span>",
                        unsafe_allow_html=True
                    )

            else:

                st.success("No gaps")


            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


        # ---------------- IMPROVEMENT SUGGESTIONS ----------------

        st.markdown(
            "### 🚀 How to Improve This Candidate's Score"
        )


        if candidate["missing_skills"]:

            impact = (
                int(
                    (
                        len(candidate["missing_skills"])
                        /
                        len(job_skills)
                    )
                    * 100
                )
                if job_skills
                else 0
            )


            st.info(
                f"Closing {len(candidate['missing_skills'])} "
                f"skill gap(s) could improve match by up to ~{impact}%"
            )


            for skill in sorted(
                candidate["missing_skills"]
            )[:3]:

                st.write(
                    f"→ Focus on **{skill}**"
                )


        else:

            st.success(
                "This candidate covers every skill in the job description."
            )


    # ---------------- ANALYTICS TAB ----------------

    with tab_analytics:

        st.markdown(
            "<div class='section-title'>Most common skill gaps across all candidates</div>",
            unsafe_allow_html=True
        )


        gap_counts = {}


        for c in ranked:

            for skill in c["missing_skills"]:

                gap_counts[skill] = (
                    gap_counts.get(skill, 0)
                    + 1
                )


        if gap_counts:

            gap_df = pd.DataFrame(

                sorted(
                    gap_counts.items(),
                    key=lambda x: x[1],
                    reverse=True
                ),

                columns=[
                    "Skill",
                    "Candidates Missing It"
                ],

            )


            gap_chart = alt.Chart(gap_df).mark_bar(
                color="#991b1b",
                cornerRadiusEnd=4
            ).encode(

                x=alt.X(
                    "Candidates Missing It:Q",
                    title="# Candidates Missing"
                ),

                y=alt.Y(
                    "Skill:N",
                    sort="-x",
                    title=None
                ),

                tooltip=[
                    "Skill",
                    "Candidates Missing It"
                ],

            ).properties(
                height=max(
                    180,
                    28 * len(gap_df)
                )
            )


            st.altair_chart(
                gap_chart,
                use_container_width=True
            )


            top_gap = gap_df.iloc[0]


            st.info(
                f"**{top_gap['Skill']}** is the most common gap — "
                f"missing from "
                f"{int(top_gap['Candidates Missing It'])} "
                f"of {len(ranked)} candidate(s)."
            )


        else:

            st.success(
                "Every candidate covers all skills mentioned in the job description."
            )


        st.divider()


        # ---------------- SCORE DISTRIBUTION ----------------

        st.markdown(
            "<div class='section-title'>Overall Score Distribution</div>",
            unsafe_allow_html=True
        )


        dist_df = pd.DataFrame({

            "Candidate": [
                c["file_name"]
                for c in ranked
            ],

            "Score": [
                round(
                    c["match_score"] * 100,
                    1
                )
                for c in ranked
            ],

        })


        dist_chart = alt.Chart(dist_df).mark_bar(
            color="#0f172a",
            cornerRadiusEnd=4
        ).encode(

            x=alt.X(
                "Candidate:N",
                sort="-y",
                title=None
            ),

            y=alt.Y(
                "Score:Q",
                title="Overall Match Score (%)",
                scale=alt.Scale(domain=[0, 100])
            ),

            tooltip=[
                "Candidate",
                "Score"
            ],

        ).properties(
            height=280
        )


        st.altair_chart(
            dist_chart,
            use_container_width=True
        )


# ---------------- WARNINGS ----------------

elif uploaded_files and not job_description:

    st.warning(
        "Paste a job description to score the uploaded resume(s)."
    )


elif job_description and not uploaded_files:

    st.warning(
        "Upload at least one resume (PDF) to get started."
    )


else:

    st.markdown(
        "<div class='card'>",
        unsafe_allow_html=True
    )

    st.write(
        "👆 Upload one or more resumes and paste a job description "
        "to see real-time scoring, skill-gap analysis, and a ranked "
        "candidate dashboard."
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )
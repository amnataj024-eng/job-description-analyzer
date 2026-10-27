"""Streamlit UI.  Run with:  streamlit run app.py"""
import html
import json
from pathlib import Path

import streamlit as st

from graph import run_analysis

st.set_page_config(page_title="Job Description Analyzer", page_icon="📄", layout="centered")

TAG_CSS = """
<style>
.tag {display:inline-block; background:#e8f0fe; color:#1a56db; padding:4px 12px;
      margin:3px 4px 3px 0; border-radius:16px; font-size:0.9rem; font-weight:500;}
.tag-top {background:#fff3cd; color:#8a6100;}
@media (prefers-color-scheme: dark) {
  .tag {background:#1e3a5f; color:#cfe0ff;}
  .tag-top {background:#4d3b00; color:#ffe9a6;}
}
</style>
"""
st.markdown(TAG_CSS, unsafe_allow_html=True)


def render_tags(items, extra_class=""):
    spans = "".join(f'<span class="tag {extra_class}">{html.escape(str(i))}</span>' for i in items)
    st.markdown(spans or "_None found_", unsafe_allow_html=True)


st.title("📄 Job Description Analyzer")
st.caption("Paste a job description and get a structured hiring report (LangGraph + LLM).")

if "text" not in st.session_state:
    st.session_state.text = ""

if st.button("Load sample job description"):
    sample = Path(__file__).parent / "sample_jd.txt"
    st.session_state.text = sample.read_text(encoding="utf-8") if sample.exists() else ""

job_text = st.text_area("Job description", key="text", height=260,
                        placeholder="Paste the full job description here...")

if st.button("Analyze", type="primary"):
    with st.spinner("Running the LangGraph workflow..."):
        st.session_state.result = run_analysis(job_text)

result = st.session_state.get("result")
if result:
    if "error" in result:
        st.error(result["error"])
    else:
        r = result["report"]
        st.divider()
        st.header(r["job_title"])
        c1, c2, c3 = st.columns(3)
        c1.metric("Company", r["company_name"])
        c2.metric("Level", r["seniority_level"])
        c3.metric("Category", r["job_category"])

        st.subheader("Required experience")
        st.write(r["required_experience"])

        st.subheader("Required skills")
        render_tags(r["required_skills"])

        st.subheader("Top 3 skills")
        for s in r["top_skills"]:
            st.markdown(f"**{s['rank']}. {html.escape(s['skill'])}**: {s['reason']}")
        render_tags([s["skill"] for s in r["top_skills"]], "tag-top")

        st.subheader("Summary")
        st.write(r["summary"])

        st.download_button("⬇️ Export report as JSON",
                           data=json.dumps(r, indent=2, ensure_ascii=False),
                           file_name="hiring_report.json", mime="application/json")
        with st.expander("View raw JSON"):
            st.json(r)

import streamlit as st
import os
from core.pipeline import run_exam_research

st.set_page_config(page_title="Gov Exam Agent", page_icon="🎓", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .status-box { padding: 10px; border-left: 5px solid #00d4ff; background: #1a1c23; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

st.title("🎓 Indian Government Exam Research Agent")
st.caption("Automated research for upcoming exams, syllabus, and prep resources.")

if "research_result" not in st.session_state:
    st.session_state.research_result = None

query = st.text_input("What exams are you looking for?", placeholder="e.g., upcoming government exams in India 2026")

if st.button("🚀 Start Research", type="primary") and query:
    with st.status("🔍 Researching...", expanded=True) as status:
        st.write("📡 Searching for upcoming exams...")
        result = run_exam_research(query)
        st.session_state.research_result = result
        status.update(label="✅ Research Complete!", state="complete")

if st.session_state.research_result:
    result = st.session_state.research_result
    
    st.download_button(
        label="💾 Download Report",
        data=result["final_report"],
        file_name="exam_report.md",
        mime="text/markdown",
    )

    tab1, tab2 = st.tabs(["📄 Final Report", "📊 Raw Data"])
    
    with tab1:
        st.markdown(result["final_report"])
    
    with tab2:
        st.subheader("Extracted Exams")
        st.json([e.dict() for e in result["extracted_exams"]])
        st.subheader("Detailed Research")
        st.json([d.dict() for d in result["detailed_info"]])

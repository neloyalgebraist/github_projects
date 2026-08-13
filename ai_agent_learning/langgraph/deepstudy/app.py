import streamlit as st
from core.pipeline import run_research

st.set_page_config(page_title="DeepStudy Pro", page_icon="🔬", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .agent-status { padding: 10px; border-left: 5px solid #00ff88; background: #1a1c23; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

st.title("🔬 DeepStudy Professional")
st.caption("Agentic Multi-Model Research Pipeline")

# --- Initialize Session State ---
if "research_result" not in st.session_state:
    st.session_state.research_result = None

query = st.text_input("What would you like to research today?", placeholder="Enter your research question...")

if st.button("🚀 Start Research", type="primary") and query:
    with st.status("🧬 Agent Pipeline Active...", expanded=True) as status:
        st.write("🧠 Orchestrator: Planning research...")
        result = run_research(query)
        st.session_state.research_result = result
        status.update(label="✅ Research Complete!", state="complete")

# --- Display Results if they exist ---
if st.session_state.research_result:
    result = st.session_state.research_result
    
    # Add Download Button in a row above the tabs
    col1, col2 = st.columns([5, 1])
    with col2:
        st.download_button(
            label="💾 Download Report",
            data=result["final_report"],
            file_name=f"research_report_{query.replace(' ', '_')[:20]}.md",
            mime="text/markdown",
        )

    tab1, tab2, tab3 = st.tabs(["📄 Final Report", "🔍 Evidence", "📊 Methodology"])
    
    with tab1:
        st.markdown(result["final_report"])
    
    with tab2:
        for i, f in enumerate(result.get("extracted_findings", [])):
            with st.expander(f"{f.get('title', 'Unknown Source')}"):
                st.write(f"**Sources:** {f.get('url', 'N/A')}")
                for p in f.get("points", []):
                    st.markdown(f"- {p}")

    with tab3:
        st.subheader("Research Plan")
        st.info(result.get("plan", "No plan generated."))
        st.subheader("Critic Assessment")
        st.warning(f"Confidence: {result.get('quality_score', 0):.0%}")
        st.write(result.get("critique", "No critique available."))

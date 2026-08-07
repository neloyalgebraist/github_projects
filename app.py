"""Streamlit front end for the multi-agent research pipeline."""

import os
import re
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

from multi_agent_research.agents.agents import AVAILABLE_MODELS, DEFAULT_MODEL
from multi_agent_research.pipelines.pipeline import STAGES, Research, stream_research

load_dotenv()

st.set_page_config(
    page_title="Multi-Agent Research",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded",
)

EXAMPLE_TOPICS = [
    "The impact of AI on the job market in 2026",
    "Small modular reactors and grid decarbonisation",
    "State of solid-state battery commercialisation",
]

STYLES = """
<style>
  :root {
    --ink:      #111827;
    --ink-soft: #4b5563;
    --ink-mute: #9ca3af;
    --line:     #e5e7eb;
    --surface:  #ffffff;
    --raised:   #f6f7fb;
    --brand:    #4338ca;
    --brand-dim:#eef2ff;
  }

  #MainMenu, footer, header [data-testid="stToolbar"] { visibility: hidden; }
  .block-container { padding-top: 2.4rem; max-width: 1180px; }

  /* ---- hero ---- */
  .hero { border-bottom: 1px solid var(--line); padding-bottom: 1.6rem; margin-bottom: 2rem; }
  .hero h1 {
    font-size: 2.35rem; font-weight: 680; letter-spacing: -0.025em;
    color: var(--ink); margin: 0 0 .45rem 0; line-height: 1.15;
  }
  .hero p { color: var(--ink-soft); font-size: 1.02rem; margin: 0; max-width: 62ch; }
  .eyebrow {
    display: inline-block; font-size: .72rem; font-weight: 640; letter-spacing: .09em;
    text-transform: uppercase; color: var(--brand); background: var(--brand-dim);
    padding: .28rem .6rem; border-radius: 999px; margin-bottom: .85rem;
  }

  /* ---- pipeline strip ---- */
  .flow { display: flex; flex-wrap: wrap; align-items: center; gap: .5rem; margin-top: 1.3rem; }
  .node {
    display: flex; align-items: baseline; gap: .45rem;
    border: 1px solid var(--line); border-radius: 8px;
    padding: .42rem .75rem; background: var(--surface);
    font-size: .84rem; color: var(--ink-soft); white-space: nowrap;
  }
  .node b { color: var(--ink); font-weight: 600; }
  .node span { color: var(--ink-mute); font-variant-numeric: tabular-nums; font-size: .74rem; }
  .arrow { color: var(--ink-mute); font-size: .9rem; }

  /* ---- metric row ---- */
  .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(155px, 1fr)); gap: .9rem; margin: .4rem 0 1.6rem; }
  .stat { border: 1px solid var(--line); border-radius: 10px; padding: .95rem 1.05rem; background: var(--raised); }
  .stat .k { font-size: .72rem; letter-spacing: .06em; text-transform: uppercase; color: var(--ink-mute); font-weight: 600; }
  .stat .v { font-size: 1.6rem; font-weight: 660; color: var(--ink); letter-spacing: -0.02em; margin-top: .2rem; line-height: 1.1; }

  /* ---- source list ---- */
  .src { border: 1px solid var(--line); border-left: 3px solid var(--brand); border-radius: 8px;
         padding: .7rem .9rem; margin-bottom: .55rem; background: var(--surface); }
  .src a { color: var(--brand); text-decoration: none; font-size: .9rem; word-break: break-all; }
  .src a:hover { text-decoration: underline; }
  .src .host { display: block; font-size: .74rem; color: var(--ink-mute); font-weight: 600;
               text-transform: uppercase; letter-spacing: .05em; margin-bottom: .2rem; }

  /* ---- report surface (st.container(border=True)) ---- */
  [data-testid="stVerticalBlockBorderWrapper"] { border-radius: 12px; }
  [data-testid="stVerticalBlockBorderWrapper"] h1,
  [data-testid="stVerticalBlockBorderWrapper"] h2,
  [data-testid="stVerticalBlockBorderWrapper"] h3 { letter-spacing: -0.015em; }
  [data-testid="stVerticalBlockBorderWrapper"] p,
  [data-testid="stVerticalBlockBorderWrapper"] li { color: var(--ink-soft); line-height: 1.72; }

  /* ---- controls ---- */
  .stButton > button {
    border-radius: 8px; font-weight: 570; border: 1px solid var(--line);
    transition: transform .06s ease, box-shadow .12s ease;
  }
  .stButton > button:hover { transform: translateY(-1px); }
  .stButton > button[kind="primary"] { box-shadow: 0 1px 2px rgba(17,24,39,.09); }
  [data-testid="stSidebar"] { border-right: 1px solid var(--line); background: var(--raised); }
  [data-testid="stSidebar"] .block-container { padding-top: 1.8rem; }
</style>
"""

st.markdown(STYLES, unsafe_allow_html=True)


def host_of(url: str) -> str:
    match = re.match(r"https?://(?:www\.)?([^/]+)", url)
    return match.group(1) if match else "source"


def score_from(feedback: str) -> str:
    match = re.search(r"Score:\s*(\d+(?:\.\d+)?)\s*/\s*10", feedback or "")
    return f"{match.group(1)}/10" if match else "—"


def missing_keys() -> list[str]:
    return [k for k in ("GROQ_API_KEY", "TAVILY_API_KEY") if not os.getenv(k)]


# ----------------------------------------------------------------- sidebar
with st.sidebar:
    st.markdown("### Configuration")
    model = st.selectbox(
        "Model",
        AVAILABLE_MODELS,
        index=AVAILABLE_MODELS.index(DEFAULT_MODEL),
        help="Served by Groq. All listed models support tool calling.",
    )
    temperature = st.slider(
        "Temperature", 0.0, 1.0, 0.0, 0.1,
        help="0 keeps the agents factual and repeatable. Raise it for looser prose.",
    )

    st.markdown("---")
    st.markdown("### Credentials")
    absent = missing_keys()
    for key in ("GROQ_API_KEY", "TAVILY_API_KEY"):
        st.markdown(f"{'❌' if key in absent else '✅'} `{key}`")
    if absent:
        st.caption("Add the missing keys to `.env`, then rerun.")

    st.markdown("---")
    st.markdown("### How it works")
    st.caption(
        "Four specialists run in sequence. The **search** and **read** agents each "
        "hold a tool and decide for themselves when to call it; the **writer** and "
        "**critic** are straight LCEL chains. Source URLs are lifted from raw tool "
        "output rather than the agents' prose, so citations survive the handoff."
    )

# ----------------------------------------------------------------- hero
st.markdown(
    f"""
    <div class="hero">
      <div class="eyebrow">LangChain · Groq · Tavily</div>
      <h1>Multi-Agent Research</h1>
      <p>Point four cooperating agents at a topic. They search the open web, read the
         strongest source in full, draft a cited report, and then critique their own work.</p>
      <div class="flow">
        {'<span class="arrow">→</span>'.join(
            f'<div class="node"><span>0{i}</span><b>{label}</b></div>'
            for i, (_, label, _) in enumerate(STAGES, 1)
        )}
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------- input
if "topic" not in st.session_state:
    st.session_state.topic = EXAMPLE_TOPICS[0]
if "result" not in st.session_state:
    st.session_state.result = None

field, action = st.columns([5, 1], vertical_alignment="bottom")
with field:
    topic = st.text_input(
        "Research topic",
        key="topic",
        placeholder="e.g. The impact of AI on the job market in 2026",
    )
with action:
    launch = st.button("Run research", type="primary", use_container_width=True)

st.caption("Try one of these:")
chips = st.columns(len(EXAMPLE_TOPICS))
for column, example in zip(chips, EXAMPLE_TOPICS):
    column.button(
        example,
        key=f"ex_{example}",
        use_container_width=True,
        on_click=lambda e=example: st.session_state.update(topic=e),
    )

st.markdown("")

# ----------------------------------------------------------------- run
if launch:
    if absent:
        st.error(f"Missing {', '.join(absent)} in `.env` — the agents cannot start.")
    elif not topic.strip():
        st.warning("Enter a topic to research.")
    else:
        st.session_state.result = None
        panels: dict[str, object] = {}
        doing = {key: verb for key, _, verb in STAGES}
        labels = {key: label for key, label, _ in STAGES}

        try:
            for item in stream_research(topic.strip(), model, temperature):
                if isinstance(item, Research):
                    st.session_state.result = item
                    break
                step = [i for i, (k, _, _) in enumerate(STAGES, 1) if k == item.stage][0]
                if item.status == "start":
                    panels[item.stage] = st.status(
                        f"**{step}/4 · {labels[item.stage]}** — {doing[item.stage]}",
                        expanded=False,
                    )
                else:
                    panel = panels[item.stage]
                    panel.update(
                        label=f"**{step}/4 · {labels[item.stage]}** — complete",
                        state="complete",
                    )
                    with panel:
                        st.markdown(item.content)
        except Exception as exc:  # surface provider/network errors in the UI
            st.error(f"The pipeline stopped: {exc}")

# ----------------------------------------------------------------- results
result: Research | None = st.session_state.result

if result:
    st.markdown("## Results")
    words = len(result.report.split())
    st.markdown(
        f"""
        <div class="stats">
          <div class="stat"><div class="k">Sources found</div><div class="v">{len(result.sources)}</div></div>
          <div class="stat"><div class="k">Report length</div><div class="v">{words:,} <span style="font-size:.85rem;color:#9ca3af">words</span></div></div>
          <div class="stat"><div class="k">Critic score</div><div class="v">{score_from(result.feedback)}</div></div>
          <div class="stat"><div class="k">Model</div><div class="v" style="font-size:.95rem;padding-top:.4rem">{result.model}</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    report_tab, sources_tab, critique_tab, trail_tab = st.tabs(
        ["Report", f"Sources ({len(result.sources)})", "Critique", "Research trail"]
    )

    with report_tab:
        with st.container(border=True):
            st.markdown(result.report or "_No report was produced._")
        stamp = datetime.now().strftime("%Y%m%d-%H%M")
        slug = re.sub(r"[^a-z0-9]+", "-", result.topic.lower()).strip("-")[:48]
        st.download_button(
            "Download report (.md)",
            data=f"# {result.topic}\n\n{result.report}\n\n## Sources\n"
            + "\n".join(f"- {u}" for u in result.sources),
            file_name=f"{slug}-{stamp}.md",
            mime="text/markdown",
        )

    with sources_tab:
        if result.sources:
            for url in result.sources:
                st.markdown(
                    f'<div class="src"><span class="host">{host_of(url)}</span>'
                    f'<a href="{url}" target="_blank">{url}</a></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("No URLs were recovered from this run.")

    with critique_tab:
        st.markdown(result.feedback or "_The critic returned nothing._")

    with trail_tab:
        st.markdown("#### Search agent — summary")
        st.markdown(result.search_summary or "_empty_")
        st.markdown("#### Search tool — raw output")
        st.code(result.search_findings or "empty", language="text")
        st.markdown("#### Reader agent — scraped content")
        st.markdown(result.scraped_content or "_empty_")
else:
    st.info("Enter a topic above and run the pipeline to see a report here.")

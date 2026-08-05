"""Streamlit front-end for the ReAct agent.

    streamlit run app.py

The point of the UI is to make the agent loop *visible*: every Thought,
Action, and Observation is rendered live as the agent works, instead of
scrolling past in a terminal.
"""

from __future__ import annotations

import streamlit as st
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

from ai_agent_learning.agent import build_agent
from ai_agent_learning.config import REQUIRED_KEYS, missing_keys

PAGE_TITLE = "ReAct Agent"
PAGE_ICON = "🧭"

MODELS = [
    "llama-3.3-70b-versatile",
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "llama-3.1-8b-instant",
]

EXAMPLES = [
    "What is the capital of India, and what is the weather there right now?",
    "What is the weather in Tokyo?",
    "What are the latest developments in AI agents?",
    "Compare the current weather in Paris and London.",
]

STYLE = """
<style>
    .block-container { padding-top: 2.5rem; max-width: 52rem; }
    #MainMenu, footer { visibility: hidden; }

    .hero { margin-bottom: 0.25rem; }
    .hero h1 {
        font-size: 2rem; font-weight: 700; margin: 0;
        letter-spacing: -0.02em;
    }
    .hero p {
        margin: 0.35rem 0 0; opacity: 0.65; font-size: 0.95rem;
    }
    .pill {
        display: inline-block; padding: 0.15rem 0.6rem; margin-right: 0.35rem;
        border-radius: 999px; font-size: 0.75rem; font-weight: 500;
        border: 1px solid rgba(128, 128, 128, 0.35); opacity: 0.85;
    }
    div[data-testid="stChatMessage"] { padding: 0.25rem 0; }
    section[data-testid="stSidebar"] { width: 20rem !important; }
</style>
"""


def render_header() -> None:
    st.markdown(STYLE, unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="hero">
          <h1>{PAGE_ICON} {PAGE_TITLE}</h1>
          <p>A model that reasons, picks tools, and loops until it has an answer.</p>
          <div style="margin-top:0.6rem">
            <span class="pill">web search</span>
            <span class="pill">live weather</span>
            <span class="pill">ReAct loop</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()


def render_sidebar() -> dict:
    """Sidebar controls. Returns the agent settings chosen by the user."""
    with st.sidebar:
        st.subheader("Configuration")

        model = st.selectbox("Model", MODELS, index=0)
        temperature = st.slider(
            "Temperature", 0.0, 1.0, 0.0, 0.1,
            help="Keep at 0. Higher values vary phrasing, which is what "
                 "breaks the format-sensitive ReAct parser.",
        )
        max_iterations = st.slider(
            "Max steps", 1, 10, 5,
            help="Circuit breaker. Caps how many tool calls the agent may "
                 "make before giving up, so a confused loop cannot run away.",
        )
        max_search_results = st.slider(
            "Search results", 1, 5, 3,
            help="Each result is fed into the model's context on every "
                 "later step — this is a cost control, not just a preference.",
        )

        st.divider()
        st.subheader("Credentials")
        absent = missing_keys()
        for name in REQUIRED_KEYS:
            if name in absent:
                st.error(f"{name} — missing", icon="⚠️")
            else:
                st.success(f"{name} — loaded", icon="✅")

        st.divider()
        if st.button("Clear conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        st.caption(
            "Each answer is independent — the agent is not given the previous "
            "turns. Conversation memory is a separate feature."
        )

    return {
        "model": model,
        "temperature": temperature,
        "max_iterations": max_iterations,
        "max_search_results": max_search_results,
    }


@st.cache_resource(show_spinner=False)
def get_agent(model: str, temperature: float, max_iterations: int, max_search_results: int):
    """Build the agent once per unique settings combination.

    Cached because assembling it fetches the ReAct prompt over the network;
    doing that on every keystroke would be slow and rude to the hub.
    """
    return build_agent(
        model=model,
        temperature=temperature,
        max_iterations=max_iterations,
        max_search_results=max_search_results,
        verbose=False,
    )


def render_examples() -> str | None:
    """Show clickable starter questions. Returns one if clicked."""
    st.caption("Try one of these:")
    chosen = None
    for row in (EXAMPLES[:2], EXAMPLES[2:]):
        for column, example in zip(st.columns(len(row)), row):
            if column.button(example, use_container_width=True):
                chosen = example
    return chosen


def answer(question: str, settings: dict) -> None:
    """Run the agent and stream its reasoning into the page."""
    with st.chat_message("assistant"):
        # StreamlitCallbackHandler renders each Thought / Action / Observation
        # into this container as the loop runs — the whole point of the UI.
        callback = StreamlitCallbackHandler(
            st.container(), expand_new_thoughts=True, collapse_completed_thoughts=True
        )
        try:
            result = get_agent(**settings).invoke(
                {"input": question}, {"callbacks": [callback]}
            )
            output = result["output"]
            steps = len(result.get("intermediate_steps", []))
        except Exception as exc:  # noqa: BLE001 — surface any failure in the UI
            output = f"The agent failed: `{exc}`"
            steps = 0

        st.markdown(output)
        if steps:
            st.caption(f"{steps} tool call{'s' if steps != 1 else ''} used")

    st.session_state.messages.append({"role": "assistant", "content": output})


def main() -> None:
    st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="centered")
    render_header()
    settings = render_sidebar()

    if missing_keys():
        st.error(
            "Missing API keys — copy `.env.example` to `.env` and fill it in. "
            "See the sidebar for which ones.",
            icon="🔑",
        )
        st.stop()

    st.session_state.setdefault("messages", [])

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    example = render_examples() if not st.session_state.messages else None
    question = st.chat_input("Ask the agent anything…") or example

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)
        answer(question, settings)


if __name__ == "__main__":
    main()

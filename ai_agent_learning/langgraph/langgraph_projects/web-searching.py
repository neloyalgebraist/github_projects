import asyncio
import operator
from typing import TypedDict, Annotated, List, Union

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langchain_community.document_loaders import WikipediaLoader
from langchain_tavily import TavilySearch
from langgraph.graph import START, END, StateGraph

# --- 1. SETUP ---
# Ensure your GROQ_API_KEY and TAVILY_API_KEY are set in your environment
llm = ChatGroq(model="llama-3.3-70b-versatile")


class State(TypedDict):
    question: str
    answer: Union[BaseMessage, dict, str]
    context: Annotated[List[str], operator.add]


# --- 2. NODES ---
def search_web(state: State):
    """Retrieve docs from web search"""
    tavily_search = TavilySearch(max_results=3)
    data = tavily_search.invoke({"query": state["question"]})
    search_docs = data.get("results", data)

    formatted = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}">\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
    )
    return {"context": [formatted]}


def search_wikipedia(state: State):
    """Retrieve docs from wikipedia"""
    search_docs = WikipediaLoader(query=state["question"], load_max_docs=2).load()

    formatted = "\n\n---\n\n".join(
        [
            f'<Document source="{doc.metadata.get("source", "N/A")}">\n{doc.page_content}\n</Document>'
            for doc in search_docs
        ]
    )
    return {"context": [formatted]}


def generate_answer(state: State):
    """Node to answer a question using accumulated context"""
    context = state.get("context", [])
    question = state["question"]

    prompt = f"Answer the question: {question}\n\nUsing this context:\n{context}"

    answer = llm.invoke(
        [
            SystemMessage(content="You are a helpful research assistant."),
            HumanMessage(content=prompt),
        ]
    )

    return {"answer": answer}


# --- 3. GRAPH DEFINITION ---
builder = StateGraph(State)

builder.add_node("search_web", search_web)
builder.add_node("search_wikipedia", search_wikipedia)
builder.add_node("generate_answer", generate_answer)

# Parallel execution
builder.add_edge(START, "search_web")
builder.add_edge(START, "search_wikipedia")
builder.add_edge("search_web", "generate_answer")
builder.add_edge("search_wikipedia", "generate_answer")
builder.add_edge("generate_answer", END)

graph = builder.compile()

# --- 4. SDK STREAMING ---
from langgraph_sdk import get_client


async def run_sdk_stream(input_query: str):
    """This requires a running LangGraph server (e.g., 'langgraph dev')"""
    try:
        client = get_client(url="http://127.0.0.1:2026")

        # Create a thread for the conversation
        thread = await client.threads.create()

        print(f"\n--- STREAMING RESULTS (SDK) ---")
        async for event in client.runs.stream(
            thread["thread_id"],
            assistant_id="parralelization",
            input={"question": input_query},
            stream_mode="values",
        ):
            if event.data:
                answer = event.data.get("answer")
                if answer:
                    # Handle both object (local) and dict (JSON from SDK) types
                    if isinstance(answer, dict):
                        content = answer.get("content", "")
                    elif hasattr(answer, "content"):
                        content = answer.content
                    else:
                        content = str(answer)
                    print(f"Update: {content[:100]}...")
    except Exception as e:
        print(f"SDK Stream Error: {e}. (Is the LangGraph server running on port 2026?)")


# --- 5. MAIN EXECUTION ---
if __name__ == "__main__":
    query = "What is graph theory and what are the best resources to understand it?"

    # Run Locally
    print("--- RUNNING LOCALLY ---")
    try:
        result = graph.invoke({"question": query})
        if "answer" in result:
            print(result["answer"].content)
    except Exception as e:
        print(f"Local Execution Error: {e}")

    # To use the SDK streaming, uncomment the line below:
    # asyncio.run(run_sdk_stream(query))

import os
from dotenv import load_dotenv

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_react_agent, AgentExecutor

from langsmith import Client

from langchain_groq import ChatGroq

load_dotenv()

# load_dotenv() fails silently if it can't find .env, so check the keys
# actually arrived instead of hitting a confusing auth error later.
for key in ("GROQ_API_KEY", "TAVILY_API_KEY"):
    if not os.getenv(key):
        raise SystemExit(
            f"{key} is not set — check that .env exists in the project root"
        )

search_tool = TavilySearchResults(max_results=3)

# --- Step 1: calling a tool directly (kept for reference) ---
# Costs a Tavily API call on every run, so it's off while we work on the agent.
# result = search_tool.invoke("Give me the latest news on AI")
# print(result)

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# --- Step 2: calling the model directly, with no tools (kept for reference) ---
# The model had no clock and couldn't answer. That gap is why agents exist.
# response = llm.invoke("What year is it?")
# print(response)

# --- Step 3: the ReAct agent — model + tools in a loop ---

# `dangerously_pull_public_prompt` belongs here, not on create_react_agent.
# The flag exists because a hub prompt is a serialized object downloaded from
# the internet: treat it as untrusted input.
prompt = Client().pull_prompt("hwchase17/react", dangerously_pull_public_prompt=True)

tools = [search_tool]

agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,  # feed format mistakes back instead of crashing
    max_iterations=5,  # circuit breaker: never loop forever
)

result = agent_executor.invoke({"input": "Find the capital of India"})
print("\nFINAL ANSWER:", result["output"])

from contextlib import contextmanager, redirect_stdout
from langchain_groq import ChatGroq
from pydantic import config


def multiply(a: int, b: int) -> int:
    """Multiply a and b.
    Args:
        a: first int
        b: second int
    """
    return a * b


def add(a: int, b: int) -> int:
    """Adds a and b.
    Args:
        a: first int
        b: second int
    """
    return a + b


def divide(a: int, b: int) -> float:
    """Divide a by b.
    Args:
        a: first int
        b: second int
    """
    return a / b


tools = [add, multiply, divide]
llm = ChatGroq(model="llama-3.3-70b-versatile")
llm_with_tools = llm.bind_tools(tools)

from IPython.display import Image, display
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

sys_msg = SystemMessage(
    content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
)


def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}


builder = StateGraph(MessagesState)

builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,
)
builder.add_edge("tools", "assistant")

memory = MemorySaver()
graph = builder.compile(checkpointer=MemorySaver())

display(Image(graph.get_graph(xray=True).draw_mermaid_png()))

initial_input = {"messages": HumanMessage(content="Multiply 2 and 3")}
thread = {"configurable": {"thread_id": "1"}}
for event in graph.stream(initial_input, thread, stream_mode="values"):
    event["messages"][-1].pretty_print()

# print(graph.get_state({"configurable": {"thread_id": "1"}}))
all_states = [s for s in graph.get_state_history(thread)]
# print(all_states)
# print(len(all_states))
#
# print(all_states[-2])

to_replay = all_states[-2]
# print(to_replay)

print(to_replay.values)
print(to_replay.next)
print(to_replay.config)

for event in graph.stream(None, to_replay.config, stream_mode="values"):
    event["messages"][-1].pretty_print()


to_fork = all_states[-2]
print(to_fork.values["messages"])
print(to_fork.config)
fork_config = graph.update_state(
    to_fork.config,
    {
        "messages": [
            HumanMessage(
                content="Multiply 5 and 3", id=to_fork.values["messages"][0].id
            )
        ]
    },
)

print(fork_config)

all_states = [state for state in graph.get_state_history(thread)]
print(all_states[0].values["messages"])
print(graph.get_state({"configurable": {"thread_id": "1"}}))

for event in graph.stream(None, fork_config, stream_mode="values"):
    event["messages"][-1].pretty_print()

print(graph.get_state({"configurable": {"thread_id": "1"}}))

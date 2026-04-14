import re
from langchain_core.tools import Tool
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
        a: int
        b: int
    """
    return a + b

def divide(a: int, b: int) -> float:
    """Divide a and b.

    Args:
        a: int
        b: int
    """
    return a / b

tools = [add, multiply, divide]
llm = ChatGroq(model="llama-3.3-70b-versatile")
llm_with_tools = llm.bind_tools(tools)

from langgraph.checkpoint import memory
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage

# System Message
sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.")

# Node
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

from langgraph.graph import START, StateGraph   
from langgraph.prebuilt import tools_condition, ToolNode
from IPython.display import Image, display
from langgraph.checkpoint.memory import MemorySaver

# graph
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges(
        "assistant",
        # If the latest messages from assistant is a tool call -> tools_condition routes to tools
        # If the latest messages from assistant is not a tool call -> tools_condition routes to END
        tools_condition,
)
builder.add_edge("tools", "assistant")
react_graph = builder.compile()
memory = MemorySaver()
react_graph_memory = builder.compile(checkpointer=memory)
# Specify a thread
config = {"configurable": {"thread_id": "1"}}

# specify an inputs
messages = [HumanMessage(content="Add 3 and 4")]

# Run 
messages = react_graph_memory.invoke({"messages": messages},config)
for m in messages['messages']: 
    m.pretty_print()

messages = [HumanMessage(content="Multiply that by 2.")]
messages = react_graph_memory.invoke({"messages": messages},config)
for m in messages['messages']:
    m.pretty_print()
# Show
display(Image(react_graph.get_graph(xray=True).draw_mermaid_png()))

# Memory
messages = [HumanMessage(content="Add 3 and 4.")]
messages = react_graph.invoke({"messages": messages})
for m in messages['messages']:
    m.pretty_print()
messages = [HumanMessage(content="Multiply that by 2.")]
messages = react_graph.invoke({"messages": messages})
for m in messages['messages']:
    m.pretty_print()





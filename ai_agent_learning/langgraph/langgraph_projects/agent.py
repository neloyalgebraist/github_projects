from langchain_core import messages
from langchain_groq import ChatGroq

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
    """Divide a and b.

    Args:
        a: first int
        b: second int
    """
    return a / b

tools = [add, multiply, divide]
llm = ChatGroq(model="llama-3.3-70b-versatile")
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)

from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage

# SystemMessage
sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.")

# Node
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}


from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from IPython.display import Image, display

# graph
builder = StateGraph(MessagesState)

# Define nodes:
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Define edges:
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
        "assistant",
        # If the latest message from assistant is a tool call -> tools_condition routes to tools
        # If the latest messaage from assistant is not a tool call -> tools_condition routes to END
        tools_condition,
)
builder.add_edge("tools", "assistant")
react_graph = builder.compile()

# Show in jupyter
display(Image(react_graph.get_graph(xray=True).draw_mermaid_png()))

messages = [HumanMessage(content="Add 3 and 4. Multiply the output by 2. Divide the output by 5")]
messages = react_graph.invoke({"messages": messages})
for m in messages['messages']:
    m.pretty_print()

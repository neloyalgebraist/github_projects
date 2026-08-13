from sys import exec_prefix
from langgraph import graph
from typing_extensions import TypedDict
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    foo: int

def node_1(State):
    print("===Node 1===")
    return {"foo": State['foo'] + 1}

builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)

graph = builder.compile()
display(Image(graph.get_graph().draw_mermaid_png()))
print(graph.invoke({"foo" : 1}))

print(State)

class State(TypedDict):
    foo: int

def node_1(state):
    print("===Node 1===")
    return {"foo": state['foo'] + 1}

def node_2(state):
    print("===Node 2===")
    return {"foo": state['foo'] + 1}

def node_3(state):
    print("===Node 3===")
    return {"foo": state['foo'] + 1}

builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_1", "node_3")
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

graph = builder.compile()
display(Image(graph.get_graph().draw_mermaid_png()))

from langgraph.errors import InvalidUpdateError
try:
    graph.invoke({"foo" : 1})
except InvalidUpdateError as e:
    print(f"InvalidUpdateError occured: {e}")

from operator import add
from typing import Annotated

class State(TypedDict):
    foo: Annotated[list[int], add]

def node_1(state):
    print("===Node 1===")
    return {"foo": [state['foo'][0] + 1]}

builder = StateGraph(State)
builder.add_node("node_1", node_1)
builer.add_edge(START, "node_1")
builder.add_edge("node_1", END)

graph = builder.compile()
display(Image(graph.get_graph().draw_mermaid_png()))
print(graph.invoke({"foo" : [1]}))

def node_1(state):
    print("===Node 1===")
    return {"foo": [state['foo'][-1] + 1]}

def node_2(state):
    print("===Node 2===")
    return {"foo": [state['foo'][-1] + 1]}

def node_3(state):
    print("===Node 3===")
    return {"foo": [state['foo'][-1] + 1]}

# Build graph
builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

# Logic
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_1", "node_3")
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

# Add
graph = builder.compile()

# View
display(Image(graph.get_graph().draw_mermaid_png()))

print(graph.invoke({"foo" : [1]}))
try: 
    graph.invoke("foo" : None})
except TypeError as e:
    print(f"TypeError occured: {e}")


# Custom Reducers
def reduce_list(left: list | None, right: list | None) -> list:
    """Safely combine two lists, handling cases where either or both inputs might be None.
        
        Args:
            left (list | None): The first list to combine, or None.
            right (list | None): The second list to combine, or None.

        Returns:
            list: A new list containing all elements from both input lists.
                    If an input is None, it's treated as an empty list.
    """
    if not left:
        left = []
    if not right:
        right = []
    return left + right

class DefaultState(TypedDict):
    foo: Annoted(list[int], add]

class CustomReducerState(TypedDict):
    foo: Annoted(list[int], reduce_list)

def node_1(state):
    print("---Node 1---")
    return {"foo": [2]}

# Build graph
builder = StateGraph(DefaultState)
builder.add_node("node_1", node_1)

# Logic
builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)

# Add
graph = builder.compile()

# View
display(Image(graph.get_graph().draw_mermaid_png()))

try:
    print(graph.invoke({"foo" : None}))
except TypeError as e:
    print(f"TypeError occurred: {e}")

from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage, HumanMessage

# Initial state
initial_messages = [AIMessage(content="Hello! How can I assist you?", name="Model"),
                    HumanMessage(content="I'm looking for information on marine biology.", name="Lance")
                   ]

# New message to add
new_message = AIMessage(content="Sure, I can help with that. What specifically are you interested in?", name="Model")

# Test
add_messages(initial_messages , new_message)

# Initial state
initial_messages = [AIMessage(content="Hello! How can I assist you?", name="Model", id="1"),
                    HumanMessage(content="I'm looking for information on marine biology.", name="Lance", id="2")
                   ]

# New message to add
new_message = HumanMessage(content="I'm looking for information on whales, specifically", name="Lance", id="2")

# Test
add_messages(initial_messages , new_message)

from langchain_core.messages import RemoveMessage

# Message list
messages = [AIMessage("Hi.", name="Bot", id="1")]
messages.append(HumanMessage("Hi.", name="Lance", id="2"))
messages.append(AIMessage("So you said you were researching ocean mammals?", name="Bot", id="3"))
messages.append(HumanMessage("Yes, I know about whales. But what others should I learn about?", name="Lance", id="4"))

# Isolate messages to delete
delete_messages = [RemoveMessage(id=m.id) for m in messages[:-2]]
print(delete_messages)
    
add_messages(messages , delete_messages)


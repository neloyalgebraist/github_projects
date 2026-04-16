from inspect import classify_class_attrs
from typing import Any, List
from langgraph import graph
from pydantic.type_adapter import R
from pydantic.warnings import TypedDictExtraConfigWarning
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
import operator
from typing import Annotated

# class State(TypedDict):
#    state: List[str]


class State(TypedDict):
    state: Annotated[list, operator.add]


class ReturnNodeValue:
    def __init__(self, node_secret: str):
        self._value = node_secret

    def __call__(self, state: State) -> Any:
        print(f"Adding {self._value} to {state['state']}")
        return {"state": [self._value]}


# Add node_secret
# builder = StateGraph(State)

# # Initialize each node with node_secret
# builder.add_node("a", ReturnNodeValue("I'm A"))
# builder.add_node("b", ReturnNodeValue("I'm B"))
# builder.add_node("c", ReturnNodeValue("I'm C"))
# builder.add_node("d", ReturnNodeValue("I'm D"))
#
# # Flow
# builder.add_edge(START, "a")
# builder.add_edge("a", "b")
# builder.add_edge("b", "c")
# builder.add_edge("c", "d")
# builder.add_edge("d", END)
# graph = builder.compile()
#
#
# print(graph.invoke({"state": []}))

# builder.add_node("a", ReturnNodeValue("I'm A"))
# builder.add_node("b", ReturnNodeValue("I'm B"))
# builder.add_node("c", ReturnNodeValue("I'm C"))
# builder.add_node("d", ReturnNodeValue("I'm D"))
#
# # Flow
# builder.add_edge(START, "a")
# builder.add_edge("a", "b")
# builder.add_edge("a", "c")
# builder.add_edge("b", "d")
# builder.add_edge("c", "d")
# builder.add_edge("d", END)
# graph = builder.compile()
#
# from langgraph.errors import InvalidUpdateError
#
# try:
#     graph.invoke({"state": []})
# except InvalidUpdateError as e:
#     print(f"An error occured: {e}")
#


# builder = StateGraph(State)
#
# builder.add_node("a", ReturnNodeValue("I'm A"))
# builder.add_node("b", ReturnNodeValue("I'm B"))
# builder.add_node("c", ReturnNodeValue("I'm C"))
# builder.add_node("d", ReturnNodeValue("I'm D"))
#
# # Flow
# builder.add_edge(START, "a")
# builder.add_edge("a", "b")
# builder.add_edge("a", "c")
# builder.add_edge("b", "d")
# builder.add_edge("c", "d")
# builder.add_edge("d", END)
# graph = builder.compile()
#
# print(graph.invoke({"state": []}))


# builder = StateGraph(State)
#
# # Initialize each node with node_secret
# builder.add_node("a", ReturnNodeValue("I'm A"))
# builder.add_node("b", ReturnNodeValue("I'm B"))
# builder.add_node("b2", ReturnNodeValue("I'm B2"))
# builder.add_node("c", ReturnNodeValue("I'm C"))
# builder.add_node("d", ReturnNodeValue("I'm D"))
#
# # Flow
# builder.add_edge(START, "a")
# builder.add_edge("a", "b")
# builder.add_edge("a", "c")
# builder.add_edge("b", "b2")
# builder.add_edge(["b2", "c"], "d")
# builder.add_edge("d", END)
# graph = builder.compile()
#
# print(graph.invoke({"state": []}))
def sorting_reducer(left, right):
    """Combines and sorts the values in a list"""
    if not isinstance(left, list):
        left = [left]

    if not isinstance(right, list):
        right = [right]

    return sorted(left + right, reverse=False)


class State(TypedDict):
    # sorting_reducer will sort the values in state
    state: Annotated[list, sorting_reducer]


# Add nodes
builder = StateGraph(State)

# Initialize each node with node_secret
builder.add_node("a", ReturnNodeValue("I'm A"))
builder.add_node("b", ReturnNodeValue("I'm B"))
builder.add_node("b2", ReturnNodeValue("I'm B2"))
builder.add_node("c", ReturnNodeValue("I'm C"))
builder.add_node("d", ReturnNodeValue("I'm D"))

# Flow
builder.add_edge(START, "a")
builder.add_edge("a", "b")
builder.add_edge("a", "c")
builder.add_edge("b", "b2")
builder.add_edge(["b2", "c"], "d")
builder.add_edge("d", END)
graph = builder.compile()

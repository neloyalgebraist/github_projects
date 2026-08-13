import re
from typing import Type
from langgraph import graph
from langgraph.pregel.main import Input
from typing_extensions import TypedDict
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END

class OverallState(TypedDict):
    foo: int

class PrivateState(TypedDict):
    baz: int

def node_1(state: OverallState) -> PrivateState:
    print("===Node 1===")
    return {"baz": state['foo'] + 1}

def node_2(state: PrivateState) -> OverallState:
    print("===Node 2===")
    return {"foo": state['baz'] + 1}

builder = StateGraph(OverallState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)

builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", END)

graph = builder.compile()

display(Image(graph.get_graph().draw_mermaid_png()))

print(graph.invoke({"foo" : 1}))


class OverallState(TypedDict):
    question: str
    answer: str
    notes: str

def thinking_node(state: OverallState):
    return {"answer": "bye", "notes": "... his name is n3l0y"}

def answer_node(state: OverallState):
    return {"answer": "bye n3l0y"}

graph = StateGraph(OverallState)
graph.add_node("answer_node", answer_node)
graph.add_node("thinking_node", thinking_node)
graph.add_edge(START, "thinking_node")
graph.add_edge("thinking_node", "answer_node")
graph.add_edge("answer_node", END)

graph = graph.compile()
display(Image(graph.get_graph().draw_mermaid_png()))

print(graph.invoke({"question" : "hi"}))


class InputState(TypedDict):
    question: str

class OutputState(TypedDict):
    answer: str

class OverallState(TypedDict):
    question: str
    answer: str
    notes: str

def thinking_node(state: InputState):
    return {"answer": "bye", "notes": "... his name is n3l0y"}

def answer_node(state: OverallState) -> OutputState:
    return {"answer": "bye n3l0y"}

graph = StateGraph(OverallState, input_schema=InputState, output_schema=OutputState)
graph.add_node("answer_node", answer_node)
graph.add_node("thinking_node", thinking_node)
graph.add_edge(START, "thinking_node")
graph.add_edge("thinking_node", "answer_node")
graph.add_edge("answer_node", END)

graph = graph.compile()

display(Image(graph.get_graph().draw_mermaid_png()))

print(graph.invoke({"question":"hi"}))

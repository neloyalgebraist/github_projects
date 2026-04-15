from os import ST_APPEND
from IPython.display import Image, display
from langgraph.checkpoint import memory
from typing_extensions import TypedDict
from langgraph.checkpoint.memory import MemorySaver
from langgraph.errors import NodeInterrupt
from langgraph.graph import START, END, StateGraph

class State(TypedDict):
    input: str

def step_1(state: State) -> State:
    print("===step 1===")
    return state

def step_2(state: State) -> State:
    if len(state['input']) > 5:
        raise NodeInterrupt(f"Received input that is longer than 5 characters: {state['input']}")

    print("===step 2===")
    return state

def step_3(state: State) -> State:
    print("===step 3===")
    return state

builder = StateGraph(State)
builder.add_node("step_1", step_1)
builder.add_node("step_2", step_2)
builder.add_node("step_3", step_3)
builder.add_edge(START, "step_1")
builder.add_edge("step_1", "step_2")
builder.add_edge("step_2", "step_3")
builder.add_edge("step_3", END)

memory = MemorySaver()

graph = builder.compile(checkpointer=memory)
display(Image(graph.get_graph().draw_mermaid_png()))


initial_input = {"input": "hello world"}
thread_config = {"configurable": {"thread_id": "1"}}

for event in graph.stream(initial_input, thread_config, stream_mode="values"):
    print(event)

state = graph.get_state(thread_config)
print(state.next)
print(state.tasks)

for event in graph.stream(None, thread_config, stream_mode="values"):
    print(event)

state = graph.get_state(thread_config)
print(state.next)

graph.update_state(
        thread_config,
        {"input": "hi"},
)

for event in graph.stream(None, thread_config, stream_mode="values"):
    print(event)



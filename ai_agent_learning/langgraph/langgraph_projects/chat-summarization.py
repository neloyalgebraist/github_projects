from subprocess import check_call
from langchain_core import messages
from langgraph import graph
from langgraph.graph import MessagesState
from langchain_groq import ChatGroq

model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
class State(MessagesState):
    summary: str

from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage, content

def call_model(state: State):
    summary = state.get("summary", "")
    
    if summary:
        system_messages = f"Summary of conversation earlier: {summary}"
        messages = [SystemMessage(content=system_messages)] + state["messages"]

    else:
        messages = state["messages"]

    response = model.invoke(messages)
    return {"messages": response}

def summarize_conversation(state: State):
    summary = state.get("summary", "")
    if summary:
        summary_messages = (
            f"This is summary of the conversation to date: {summary}\n\n" 
            "Extend the summary by taking into account the new messages above:" 
        )

    else:
        summary_message = "Create a summary of the conversation above:"
    messages = state["messages"] + [HumanMessage(content=summary_message_)]
    response = model.invoke(messages)
    
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"summary": response.content, "messages": delete_messages}

from langgraph.graph import END
from typing_extensions import Literal

def should_continue(state: State) -> Literal ["summarize_conversation",END]:
    """Return the next node to execute."""
    messages = state["messages"]
    if len(messages) > 6:
        return "summarize_conversation"

    return END

from IPython.display import Image, display
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START

workflow = StateGraph(State)
workflow.add_node("conversation", call_model)
workflow.add_node(summarize_conversation)

workflow.add_edge(START, "conversation")
workflow.add_conditional_edges("conversation", should_continue)
workflow.add_edge("summarize_conversation", END)

memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)
display(Image(graph.get_graph().draw_mermaid_png()))

config = {"configurable": {"thread_id": "1"}}
input_message = HumanMessage(content="hi! I'm Lance")
output = graph.invoke({"messages": [input_message]}, config)
for m in output['messages'][-1:]:
    m.pretty_print()

graph.get_state(config).values.get("summary","")

input_message = HumanMessage(content="I like Nick Bosa, isn't he the highest paid defensive player?")
output = graph.invoke({"messages": [input_message]},config)
for m in output['messages'][-1:]:
    m.pretty_print()

graph.get_state(config).values.get("summary", "")




import asyncio
from dataclasses import astuple
from subprocess import check_call
from typing import Literal

from langchain_core import messages
from langchain_core.language_models.chat_models import agenerate_from_stream
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage, content
from langchain_core.runnables import RunnableConfig

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState

# LLM - Ensure you have GROQ_API_KEY in your environment
model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# State 
class State(MessagesState):
    summary: str

# Define the logic to call the model
def call_model(state: State, config: RunnableConfig):
    summary = state.get("summary", "")
    if summary:
        system_message = f"Summary of conversation earlier: {summary}"
        msg_list = [SystemMessage(content=system_message)] + state["messages"]
    else:
        msg_list = state["messages"]

    response = model.invoke(msg_list, config)
    return {"messages": response}

def summarize_conversation(state: State):
    summary = state.get("summary", "")
    if summary:
        summary_message = (
                f"This is summary of the conversation to date: {summary}\n\n" 
                "Extend the summary by taking into account the new messages above:" 
        )
    else:
        summary_message = "Create a summary of the conversation above:"

    msg_list = state["messages"] + [HumanMessage(content=summary_message)]
    response = model.invoke(msg_list)

    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"summary": response.content, "messages": delete_messages}

def should_continue(state: State) -> Literal["summarize_conversation", END]:
    messages = state["messages"]
    if len(messages) > 6:
        return "summarize_conversation"
    return END

# Define and Compile Graph
workflow = StateGraph(State)
workflow.add_node("conversation", call_model)
workflow.add_node("summarize_conversation", summarize_conversation)

workflow.add_edge(START, "conversation")
workflow.add_conditional_edges("conversation", should_continue)
workflow.add_edge("summarize_conversation", END)

memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)

# Main Async Function to handle streaming
async def run_streaming_examples():
    # Thread 1: Updates mode
    print("\n--- Thread 1: Updates Mode ---")
    config1 = {"configurable": {"thread_id": "1"}}
    for chunk in graph.stream({"messages": [HumanMessage(content="hi! I'm Lance")]}, config1, stream_mode="updates"):
        print(chunk)

    # Thread 2: Values mode
    print("\n--- Thread 2: Values Mode ---")
    config2 = {"configurable": {"thread_id": "2"}}
    input_msg2 = HumanMessage(content="hi! I'm Lance")
    for event in graph.stream({"messages": [input_msg2]}, config2, stream_mode="values"):
        if 'messages' in event:
            for m in event['messages']:
                m.pretty_print()
        print("---" * 10)

    # Thread 3: Async Events (THE FIX)
    print("\n--- Thread 3: astream_events ---")
    config3 = {"configurable": {"thread_id": "3"}}
    input_msg3 = HumanMessage(content="Tell me about hacking the active directory")
    
    async for event in graph.astream_events({"messages": [input_msg3]}, config3, version="v2"):
        node = event['metadata'].get('langgraph_node', '')
        event_type = event['event']
        name = event['name']
        if node:
            print(f"Node: {node:15} | Type: {event_type:20} | Name: {name}")
    

    node_to_stream = 'conversation'
    config = {"configurable": {"thread_id": "4"}}
    input_message = HumanMessage(content="Tell me about the cricket match")
    async for event in graph.astream_events({"messages": [input_message]}, config, version="v2"):
        # Get chat models token from a particular node
        if event["event"] == "on_chat_model_stream" and event['metadata'].get('langgraph_node','') == node_to_stream:
            print(event['data'])

    config = {"configurable": {"thread_id": "5"}}
    input_message = HumanMessage(content="Tell me about quantum mechanics")
    async for event in graph.astream_events({"messages": [input_message]}, config, version="v2"):
        if event["event"] == "on_chat_model_stream" and event['metadata'].get('langgraph_node', '') == node_to_stream:
            data = event["data"]
            print(data["chunk"].content, end="|")


if __name__ == "__main__":
    # Run the async event loop
    asyncio.run(run_streaming_examples())





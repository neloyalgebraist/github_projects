from pprint import pprint
from langchain_core.messages import AIMessage, HumanMessage, RemoveMessage, trim_messages
from langchain_groq import ChatGroq
from IPython.display import Image, display
from langgraph.graph import MessagesState, StateGraph, START, END

# Initialize the LLM
llm = ChatGroq(model="llama-3.3-70b-versatile")

# --- Initial Message Setup ---
messages = [AIMessage(content="So you said you were researching ocean mammals?", name="n3l0y")]
messages.append(HumanMessage(content="Yes, I know about whales. But what others should I learn about?", name="n3l0y"))

for m in messages:
    m.pretty_print()

# --- Graph 1: Simple Chat Node ---
def chat_model_node(state: MessagesState):
    # We return a list so the MessageState appends it
    return {"messages": [llm.invoke(state["messages"])]}

builder = StateGraph(MessagesState)
builder.add_node("chat_model", chat_model_node)
builder.add_edge(START, "chat_model")
builder.add_edge("chat_model", END)
graph = builder.compile()

# display(Image(graph.get_graph().draw_mermaid_png())) # Uncomment if in Jupyter

output = graph.invoke({'messages': messages})
for m in output['messages']:
    m.pretty_print()

# --- Graph 2: Message Filtering (Manual Deletion) ---
def filter_messages(state: MessagesState):
    # RemoveMessage requires an 'id' to know which message to delete
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"messages": delete_messages}

def chat_model_node_v2(state: MessagesState):
    return {"messages": [llm.invoke(state["messages"])]}

builder = StateGraph(MessagesState)
builder.add_node("filter", filter_messages)
builder.add_node("chat_model", chat_model_node_v2)
builder.add_edge(START, "filter")
builder.add_edge("filter", "chat_model")
builder.add_edge("chat_model", END)
graph_filter = builder.compile()

# Example messages with IDs for the filter graph
messages_with_ids = [
    AIMessage("Hi.", name="Bot", id="1"),
    HumanMessage("Hi.", name="Lance", id="2"),
    AIMessage("So you said you were researching ocean mammals?", name="Bot", id="3"),
    HumanMessage("Yes, I know about whales. But what others should I learn about?", name="Lance", id="4")
]

output = graph_filter.invoke({'messages': messages_with_ids})
for m in output['messages']:
    m.pretty_print()

# --- Graph 3: Context Truncation (Last Message Only) ---
def chat_model_node_v3(state: MessagesState):
    # Only pass the very last message to the LLM
    return {"messages": [llm.invoke(state["messages"][-1:])]}

builder = StateGraph(MessagesState)
builder.add_node("chat_model", chat_model_node_v3)
builder.add_edge(START, "chat_model")
builder.add_edge("chat_model", END)
graph_v3 = builder.compile()

# Update conversation history
messages_with_ids.append(output['messages'][-1])
messages_with_ids.append(HumanMessage(content="Tell me more about Narwhals!", name="Lance"))

output = graph_v3.invoke({'messages': messages_with_ids})
for m in output['messages']:
    m.pretty_print()

# --- Graph 4: Using trim_messages ---
def chat_model_node_trim(state: MessagesState):
    # Trims messages to fit within a token limit
    trimmed = trim_messages(
        state["messages"],
        max_tokens=100,
        strategy="last",
        token_counter=llm, # Uses the Groq model to count tokens
        allow_partial=False,
    )
    return {"messages": [llm.invoke(trimmed)]}

builder = StateGraph(MessagesState)
builder.add_node("chat_model", chat_model_node_trim)
builder.add_edge(START, "chat_model")
builder.add_edge("chat_model", END)
graph_trim = builder.compile()

# Final Test
messages_with_ids.append(output['messages'][-1])
messages_with_ids.append(HumanMessage(content="Tell me where Orcas live!", name="Lance"))

# Demonstrate manual trimming
trimmed_manual = trim_messages(
    messages_with_ids,
    max_tokens=100,
    strategy="last",
    token_counter=llm,
    allow_partial=False
)

final_output = graph_trim.invoke({'messages': messages_with_ids})
print(final_output)

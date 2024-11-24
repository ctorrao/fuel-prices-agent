from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode

from tools import *

tools = [get_districts, get_municipalities, get_brands, get_fuel_prices, get_fuel_prices_by_brand, convert_euros_to_dollars]

# Define LLM with bound tools
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)

# System message
sys_msg = SystemMessage(
    content=(
        "You are a helpful assistant tasked with finding the fuel stations prices by category "
        "(petrol or diesel), for a given district or municipalities."
        "There is an hierichy regarding district and municipality. The district have a list of municipalities."
        "Optionally the user can specify the brand of the fuel station."
        "The default district is Lisbon and the default category is petrol."
        "When you are returing station information always include the Google Maps link."
    )
)

# Node
def assistant(state: MessagesState):
   return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", "assistant")

# Compile graph
graph = builder.compile()

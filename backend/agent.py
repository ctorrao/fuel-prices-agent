from langchain_core.messages import SystemMessage, AIMessage
from langchain_openai import ChatOpenAI

from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode

import inspect
import tools

#tools_for_llm = [tools.get_districts, tools.get_municipalities, tools.get_brands, tools.get_fuel_prices, tools.get_fuel_prices_by_brand, tools.convert_currency, tools.available_currencies_to_convert]
tools_for_llm = [
    func for name, func in inspect.getmembers(tools, inspect.isfunction)
    if func.__doc__  # Ensure the function has a docstring
]

# Define LLM with bound tools
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools_for_llm)

# System message
sys_msg = SystemMessage(
    content=(
        "You are a helpful assistant tasked with finding the fuel stations prices by category "
        "(petrol or diesel), for a given district or municipalities."
        "There is an hierarchy regarding district and municipality. The district have a list of municipalities."
        "The user can specify the district or the municipality. Compare the user given location with all the municipalities "
        "and all districts, if you do not find a match, then answer that you didn't find any match for that location."
        "Optionally the user can specify the brand of the fuel station."
        "The default district is Lisbon and the default category is petrol."
        "When you are returning station information always include the Google Maps link."
    )
)

# Greeting message
greeting_msg = AIMessage(
    content=(
        "Hello! I am a assistant to find the fuel stations prices by fuel type (petrol or diesel), for a given district or municipalities. "
        "Optionally you can filter by fuel brand.\n"
        "Try some examples:\n'prices in Lisbon',\n'diesel prices in Lisbon for Galp',\n'petrol prices'"
    )
)

# Greeting Node
def greeting(state: MessagesState):
    # is the first message?
    if state["messages"]:
        return {"messages": [greeting_msg]}
    else:
        return {"messages": []}

# Assistant Node
def assistant(state: MessagesState):
   return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

# Build graph
builder = StateGraph(MessagesState)
#builder.add_node("greeting", greeting)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools_for_llm))
builder.add_edge(START, "assistant")
#builder.add_edge(START, "greeting")
#builder.add_edge("greeting", "assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", "assistant")

# Compile graph
graph = builder.compile()

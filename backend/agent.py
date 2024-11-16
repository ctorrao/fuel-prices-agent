from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode
import requests

petrol_fuel_id = 3201
diesel_fuel_id = 2101
max_fuel_results = 10

# Districts
dict_distritos = {
    "Aveiro": 1,
    "Beja": 2,
    "Braga": 3,
    "Bragança": 4,
    "Castelo Branco": 5,
    "Coimbra": 6,
    "Évora": 7,
    "Faro": 8,
    "Guarda": 9,
    "Leiria": 10,
    "Lisboa": 11,
    "Lisbon": 11,
    "Portalegre": 12,
    "Porto": 13,
    "Santarém": 14,
    "Setúbal": 15,
    "Viana do Castelo": 16,
    "Vila Real": 17,
    "Viseu": 18
}

def get_district_id(district: str) -> int:
    """Get district id based on district name.
    Available districts: Aveiro, Beja, Braga, Bragança, Castelo Branco, Coimbra, Évora, Faro, Guarda, Leiria, Lisboa, Lisbon, Portalegre, Porto, Santarém, Setúbal, Viana do Castelo, Vila Real, Viseu

    Args:
        district: name of district
    """
    if district in dict_distritos:
        return dict_distritos[district]
    else:
        raise ValueError("Invalid district name")

def get_municipaly_ids(district: str) -> list[int]:
    """Get municipality ids based on district name.
    Available districts: Aveiro, Beja, Braga, Bragança, Castelo Branco, Coimbra, Évora, Faro, Guarda, Leiria, Lisboa, Lisbon, Portalegre, Porto, Santarém, Setúbal, Viana do Castelo, Vila Real, Viseu

    Args:
        district: name of district
    """
    ids = list[int]()
    if district in dict_distritos:
        response = requests.get(f"https://precoscombustiveis.dgeg.gov.pt/api/PrecoComb/GetMunicipios?idDistrito={dict_distritos[district]}")
        data = response.json()
        if data and "resultado" in data and len(data["resultado"]) > 0:
            for result in data["resultado"]:
                municipaly_id = result["Id"]
                municipaly_name = result["Descritivo"]
                ids.append(str(f"Id: {municipaly_id} | Name: {municipaly_name}"))
            return ids
        else:
            raise ValueError("Failed to get municipaly ids from API.")
    else:
        raise ValueError("Invalid district name")

def get_fuel_prices(category: str, district_id: int, municipality_ids: list[int]) -> list[str]:
    """Get fuel prices (in euros) based on category, district and municipalies.

    Args:
        category: type of fuel (petrol, diesel)
        district_id: district id (default is 11 for Lisbon)
        municipality_ids: list of municipality ids
    """
    prices = list[str]()
    if (municipality_ids is None) or (len(municipality_ids) == 0):
        municipality_ids_str = ""
    else:
        municipality_ids_str = "%2C".join(map(str, municipality_ids))
    if category == "petrol":
        response = requests.get(f"https://precoscombustiveis.dgeg.gov.pt/api/PrecoComb/PesquisarPostos?idsTiposComb={petrol_fuel_id}&idMarca=&idTipoPosto=&idDistrito={district_id}&idsMunicipios={municipality_ids_str}&qtdPorPagina={max_fuel_results}&pagina=1")
        data = response.json()
        if data and "resultado" in data and len(data["resultado"]) > 0:
            for result in data["resultado"]:
                prices.append(result)
            return prices[:max_fuel_results]
        else:
            raise ValueError("Failed to get gas price from API.")
    elif category == "diesel":
        response = requests.get(f"https://precoscombustiveis.dgeg.gov.pt/api/PrecoComb/PesquisarPostos?idsTiposComb={petrol_fuel_id}&idMarca=&idTipoPosto=&idDistrito={district_id}&idsMunicipios={municipality_ids_str}&qtdPorPagina={max_fuel_results}&pagina=1")
        data = response.json()
        if data and "resultado" in data and len(data["resultado"]) > 0:
            for result in data["resultado"]:
                prices.append(result)
            return prices[:max_fuel_results]
        else:
            raise ValueError("Failed to get gas price from API.")
    else:
        raise ValueError("Invalid gas category")

def convert_euros_to_dollars(euros: float) -> float:
    """Convert euros (EUR) to dollars (USD).

    Args:
        euros: amount in euros (EUR)
    """
    #usd = float(euros.trim(' ', '€')) * 1.13
    usd = euros * 1.13
    return usd

# output = get_gas_prices("regular", 11, [])
# print(output)

tools = [get_municipaly_ids, get_fuel_prices, convert_euros_to_dollars]

# Define LLM with bound tools
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)

# System message
sys_msg = SystemMessage(content="You are a helpful assistant tasked with finding the fuel prices by category (petrol or diesel), for a given district and municipality. The default district is Lisbon and the default category is petrol.")

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

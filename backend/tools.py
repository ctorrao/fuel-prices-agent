from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from datetime import datetime
import requests
import utils
import urllib.parse

petrol_fuel_id = 3201
diesel_fuel_id = 2101
max_fuel_results = 10
max_address_results = 5

def get_web_future_fuel_prices_changes() -> str:
    """Search the web to know future (tipically for next week) fuel prices flutuations or differences."""
    # Search
    tavily_search = TavilySearchAPIWrapper() #TavilySearchResults(max_results=3, include_raw_content=True)
    
    search_query = f"Preços combustiveis na próxima semana on site:contaspoupanca.pt"
    #search_docs = tavily_search.invoke(search_instructions)
    search_docs = tavily_search.raw_results(search_query, max_results=1, include_raw_content=True)
    
    # Format
    formatted_search_docs = f"\n\nDate Today: {datetime.today().strftime('%Y-%m-%d')}\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["raw_content"]}</Document>'
            for doc in search_docs["results"]
        ]
    )

    return formatted_search_docs

def get_districts_and_municipalities() -> list[str]:
    """Get all districts and municipalities names and ids."""
    districts = list[str]()
    response = requests.get("https://precoscombustiveis.dgeg.gov.pt/api/PrecoComb/GetDistritos")
    data = utils.process_api_fuel_generic_response(response)
    if data and len(data) > 0:
        for result in data:
            municipalities = list[str]()
            response = requests.get(f"https://precoscombustiveis.dgeg.gov.pt/api/PrecoComb/GetMunicipios?idDistrito={result['Id']}")
            municipalities = utils.process_api_fuel_generic_response(response)
            result["Municipalities"] = municipalities
            districts.append(result)
        return districts
    else:
        raise ValueError("Failed to get districts or municipalities from API.")

def get_brands() -> list[str]:
    """Get fuel brands."""
    brands = list[str]()
    response = requests.get("https://precoscombustiveis.dgeg.gov.pt/api/PrecoComb/GetMarcas")
    data = utils.process_api_fuel_generic_response(response)
    if data and len(data) > 0:
        for result in data:
            brands.append(result)
        return brands
    else:
        raise ValueError("Failed to get fuel brands from API.")

def get_fuel_prices_by_brand(category: str, district_id: int, municipality_ids: list[int], brand_id: int) -> list[str]:
    """Get fuel prices (in euros) based on category, district, municipalies and a single brand.

    Args:
        category: type of fuel (petrol, diesel)
        district_id: district id (default is 11 for Lisbon)
        municipality_ids: list of municipality ids (default is empty for all municipalities)
        brand_id: brand id (default is 0 for all brands)
    """
    brand_id_str = "" if brand_id == 0 else str(brand_id)
    if (municipality_ids is None) or (len(municipality_ids) == 0):
        municipality_ids_str = ""
    else:
        municipality_ids_str = "%2C".join(map(str, municipality_ids))
    if category == "petrol":
        response = requests.get(f"https://precoscombustiveis.dgeg.gov.pt/api/PrecoComb/PesquisarPostos?idsTiposComb={petrol_fuel_id}&idMarca={brand_id_str}&idTipoPosto=&idDistrito={district_id}&idsMunicipios={municipality_ids_str}&qtdPorPagina={max_fuel_results}&pagina=1")
        return utils.process_api_fuel_price_response(response, max_fuel_results)
    elif category == "diesel":
        response = requests.get(f"https://precoscombustiveis.dgeg.gov.pt/api/PrecoComb/PesquisarPostos?idsTiposComb={diesel_fuel_id}&idMarca={brand_id_str}&idTipoPosto=&idDistrito={district_id}&idsMunicipios={municipality_ids_str}&qtdPorPagina={max_fuel_results}&pagina=1")
        return utils.process_api_fuel_price_response(response, max_fuel_results)
    else:
        raise ValueError("Invalid gas category")

def get_fuel_prices(category: str, district_id: int, municipality_ids: list[int]) -> list[str]:
    """Get fuel prices (in euros) based on category, district and municipalies.

    Args:
        category: type of fuel (petrol, diesel)
        district_id: district id (default is 11 for Lisbon)
        municipality_ids: list of municipality ids (default is empty for all municipalities)
    """
    return get_fuel_prices_by_brand(category, district_id, municipality_ids, 0)

def available_currencies_to_convert() -> list[tuple[str, str]]:
    """Get all available currencies possible to convert."""
    currencies = list[tuple[str, str]]()
    response = requests.get("https://api.frankfurter.dev/v1/currencies")
    data = utils.process_api_currency_generic_response(response)
    for currency in data.items():
        currencies.append((currency[0],currency[1]))
    return currencies

def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """Convert currency from one to another.

    Args:
        amount: amount to convert
        from_currency: currency symbol to convert from
        to_currency: currency symbol to convert to
    """
    response = requests.get(f"https://api.frankfurter.dev/v1/latest?&amount={str(amount)}&base={from_currency}&symbols={to_currency}")
    data = utils.process_api_currency_generic_response(response)
    return data["rates"][to_currency]
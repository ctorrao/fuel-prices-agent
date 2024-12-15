import requests
from utils import *

petrol_fuel_id = 3201
diesel_fuel_id = 2101
max_fuel_results = 10

def get_districts() -> list[str]:
    """Get all districts names and ids."""
    districts = list[str]()
    response = requests.get("https://precoscombustiveis.dgeg.gov.pt/api/PrecoComb/GetDistritos")
    data = process_api_fuel_generic_response(response)
    if data and len(data) > 0:
        for result in data:
            districts.append(result)
        return districts
    else:
        raise ValueError("Failed to get districts from API.")

def get_municipalities(district_id: int) -> list[str]:
    """Get all municipalities from a specific district.

    Args:
        district_id: id of the district
    """
    municipalities = list[str]()
    response = requests.get(f"https://precoscombustiveis.dgeg.gov.pt/api/PrecoComb/GetMunicipios?idDistrito={district_id}")
    data = process_api_fuel_generic_response(response)
    if data and len(data) > 0:
        for result in data:
            municipalities.append(result)
        return municipalities
    else:
        raise ValueError("Failed to get municipalities from API.")

def get_brands() -> list[str]:
    """Get fuel brands."""
    brands = list[str]()
    response = requests.get("https://precoscombustiveis.dgeg.gov.pt/api/PrecoComb/GetMarcas")
    data = process_api_fuel_generic_response(response)
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
        municipality_ids: list of municipality ids
        brand_id: brand id (default is 0 for all brands)
    """
    brand_id_str = "" if brand_id == 0 else str(brand_id)
    if (municipality_ids is None) or (len(municipality_ids) == 0):
        municipality_ids_str = ""
    else:
        municipality_ids_str = "%2C".join(map(str, municipality_ids))
    if category == "petrol":
        response = requests.get(f"https://precoscombustiveis.dgeg.gov.pt/api/PrecoComb/PesquisarPostos?idsTiposComb={petrol_fuel_id}&idMarca={brand_id_str}&idTipoPosto=&idDistrito={district_id}&idsMunicipios={municipality_ids_str}&qtdPorPagina={max_fuel_results}&pagina=1")
        return process_api_fuel_price_response(response, max_fuel_results)
    elif category == "diesel":
        response = requests.get(f"https://precoscombustiveis.dgeg.gov.pt/api/PrecoComb/PesquisarPostos?idsTiposComb={diesel_fuel_id}&idMarca={brand_id_str}&idTipoPosto=&idDistrito={district_id}&idsMunicipios={municipality_ids_str}&qtdPorPagina={max_fuel_results}&pagina=1")
        return process_api_fuel_price_response(response, max_fuel_results)
    else:
        raise ValueError("Invalid gas category")

def get_fuel_prices(category: str, district_id: int, municipality_ids: list[int]) -> list[str]:
    """Get fuel prices (in euros) based on category, district and municipalies.

    Args:
        category: type of fuel (petrol, diesel)
        district_id: district id (default is 11 for Lisbon)
        municipality_ids: list of municipality ids
    """
    return get_fuel_prices_by_brand(category, district_id, municipality_ids, 0)

#def convert_euros_to_dollars(euros: float) -> float:
#    """Convert euros (EUR) to dollars (USD).
#
#    Args:
#        euros: amount in euros (EUR)
#    """
#    usd = euros * 1.13
#    return usd

def available_currencies_to_convert() -> list[tuple[str, str]]:
    """Get all available currencies possible to convert."""
    currencies = list[tuple[str, str]]()
    response = requests.get("https://api.frankfurter.dev/v1/currencies")
    data = process_api_currency_generic_response(response)
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
    data = process_api_currency_generic_response(response)
    return data["rates"][to_currency]
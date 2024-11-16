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

def get_municipaly_ids(district: str) -> list[str]:
    """Get municipality ids based on district name.
    Available districts: Aveiro, Beja, Braga, Bragança, Castelo Branco, Coimbra, Évora, Faro, Guarda, Leiria, Lisboa, Lisbon, Portalegre, Porto, Santarém, Setúbal, Viana do Castelo, Vila Real, Viseu

    Args:
        district: name of district
    """
    ids = list[str]()
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

def get_brands() -> list[str]:
    """Get fuel brands."""
    brands = list[str]()
    response = requests.get("https://precoscombustiveis.dgeg.gov.pt/api/PrecoComb/GetMarcas")
    data = response.json()
    if data and "resultado" in data and len(data["resultado"]) > 0:
        for result in data["resultado"]:
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
    prices = list[str]()
    if (municipality_ids is None) or (len(municipality_ids) == 0):
        municipality_ids_str = ""
    else:
        municipality_ids_str = "%2C".join(map(str, municipality_ids))
    if category == "petrol":
        response = requests.get(f"https://precoscombustiveis.dgeg.gov.pt/api/PrecoComb/PesquisarPostos?idsTiposComb={petrol_fuel_id}&idMarca={brand_id_str}&idTipoPosto=&idDistrito={district_id}&idsMunicipios={municipality_ids_str}&qtdPorPagina={max_fuel_results}&pagina=1")
        data = response.json()
        if data and "resultado" in data and len(data["resultado"]) > 0:
            for result in data["resultado"]:
                prices.append(result)
            return prices[:max_fuel_results]
        else:
            raise ValueError("Failed to get gas price from API.")
    elif category == "diesel":
        response = requests.get(f"https://precoscombustiveis.dgeg.gov.pt/api/PrecoComb/PesquisarPostos?idsTiposComb={diesel_fuel_id}&idMarca={brand_id_str}&idTipoPosto=&idDistrito={district_id}&idsMunicipios={municipality_ids_str}&qtdPorPagina={max_fuel_results}&pagina=1")
        data = response.json()
        if data and "resultado" in data and len(data["resultado"]) > 0:
            for result in data["resultado"]:
                prices.append(result)
            return prices[:max_fuel_results]
        else:
            raise ValueError("Failed to get gas price from API.")
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

def convert_euros_to_dollars(euros: float) -> float:
    """Convert euros (EUR) to dollars (USD).

    Args:
        euros: amount in euros (EUR)
    """
    usd = euros * 1.13
    return usd

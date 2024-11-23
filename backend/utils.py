def process_api_fuel_price_response(response, max_fuel_results):
    prices = list[str]()
    data = response.json()
    if data and "resultado" in data and len(data["resultado"]) > 0:
        for result in data["resultado"]:
            # example: https://www.google.com/maps/search/39.223868,-9.076041
            # add a google maps link using latitude and longitude
            latitude = result["Latitude"]
            longitude = result["Longitude"]
            result["GoogleMapsLink"] = f"https://www.google.com/maps/search/{latitude},{longitude}"
            prices.append(result)
        return prices[:max_fuel_results]
    else:
        raise ValueError("Failed to get gas price from API.")

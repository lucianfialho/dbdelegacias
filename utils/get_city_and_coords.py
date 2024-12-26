# utils/get_city_and_coords.py
import re
from utils.http import fetch_json

def get_city_and_coordinates_by_cep(address):
    """Extrai o CEP do endereço, busca município e coordenadas via BrasilAPI."""
    if not address:
        return "Desconhecido", None

    # Extrair o CEP com regex
    match = re.search(r"\b\d{5}-\d{3}\b", address)
    if not match:
        return "Desconhecido", None

    cep = match.group(0).replace("-", "")  # Remove o hífen
    print(f"Fetching city and coordinates for CEP: {cep}")

    # Buscar o CEP na BrasilAPI (v2)
    response = fetch_json(f"https://brasilapi.com.br/api/cep/v2/{cep}")
    if response and "city" in response:
        coordinates = None
        if "location" in response and "coordinates" in response["location"]:
            coordinates = {
                "latitude": response["location"]["coordinates"].get("latitude"),
                "longitude": response["location"]["coordinates"].get("longitude")
            }
        return response["city"], coordinates

    return "Desconhecido", None
from utils.strings import slugify
from utils.http import fetch_json
from settings import BASE_URLS, RJ_CATEGORIES
from states.base import BaseState
import re

class RioDeJaneiro(BaseState):
    def __init__(self):
        super().__init__(uf="RJ", label="Rio de Janeiro", slug="rio-de-janeiro")

    def fetch_data(self):
        for category in RJ_CATEGORIES:
            print(f"Fetching data for category: {category}")

            # Fetch JSON e extrair a lista de delegacias
            response = fetch_json(f"{BASE_URLS['RJ']}/delegacias", {
                "categoria": category,
                "column": "numero_dp",
                "direction": "ASC"
            })

            delegacias = response.get("delegacias", [])
            
            if not isinstance(delegacias, list):
                print(f"Unexpected response format for category {category}: {response}")
                continue

            for delegacy in delegacias:
                if not isinstance(delegacy, dict):
                    print(f"Skipping invalid item: {delegacy}")
                    continue  # Evita itens que não sejam dicionários

                # Identificar o município e buscar informações extras
                city, coordinates = self.get_city_and_coordinates_by_cep(delegacy.get("endereco"))

                # Ignorar delegacias cujo CEP não foi encontrado
                if city == "Desconhecido":
                    print(f"Skipping due to missing CEP: {delegacy.get('endereco')}")
                    continue

                # Adicionar dados agrupados por cidade
                self.add_city(slugify(city), [{
                    "name": f"{delegacy.get('numero_dp', '')}ª DP - {delegacy.get('localizacao', '')}",
                    "address": delegacy.get("endereco"),
                    "phone": delegacy.get("telefone") or delegacy.get("celular"),
                    "responsible": delegacy.get("responsavel"),
                    "link": delegacy.get("link"),
                    "category": category,
                    "coordinates": coordinates  # Adiciona latitude/longitude, se disponível
                }])

        print("Data fetching completed for Rio de Janeiro.")

    def get_city_and_coordinates_by_cep(self, address):
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

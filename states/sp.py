from utils.http import fetch_html, fetch_json
from utils.strings import slugify
from settings import BASE_URLS, SP_MUNICIPES
from states.base import BaseState
import re
from bs4 import BeautifulSoup

class SaoPaulo(BaseState):
    def __init__(self):
        super().__init__(uf="SP", label="São Paulo", slug="sao-paulo")

    def fetch_data(self):
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://dipol.policiacivil.sp.gov.br",
            "Referer": "https://dipol.policiacivil.sp.gov.br/sup/consulta/unidades_policiais.php",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }

        for ibge_code, city in SP_MUNICIPES.items():
            print(f"Fetching data for city: {city} ({ibge_code})")
            try:
                # Requisição POST com o código IBGE
                url = f"{BASE_URLS['SP']}/consulta/unidades.php"
                response_text = fetch_html(
                    url,
                    params={"ibge": ibge_code},
                    method="POST",
                    headers=headers
                )
                
                if not response_text:
                    print(f"Empty response for city: {city}")
                    continue

                # Fazer parsing do HTML com BeautifulSoup
                soup = BeautifulSoup(response_text, 'html.parser')
                unidades = soup.find_all('div', class_='list-group-item unidade')

                # Itera sobre as unidades retornadas no HTML
                for unit in unidades:
                    name = unit.find('h6').get_text(strip=True)
                    address_raw = unit.find('p', class_='mb-1').get_text(" ", strip=True)
                    telefone_raw = unit.find_all('p', class_='mb-1')[1].get_text(" ", strip=True)

                    # Ajuste para capturar o CEP corretamente
                    address_match = re.search(r"CEP:\s*(\d{8})", address_raw)
                    cep = address_match.group(1) if address_match else None

                    # Buscar cidade e coordenadas pelo CEP
                    city_name, coordinates = self.get_city_and_coordinates_by_cep(cep)

                    # Ignorar unidades cujo CEP não foi encontrado
                    if city_name == "Desconhecido":
                        print(f"Skipping due to missing CEP: {address_raw}")
                        continue

                    # Adicionar dados agrupados por cidade
                    self.add_city(slugify(city_name), [{
                        "name": name,
                        "address": address_raw,
                        "phone": telefone_raw,
                        "coordinates": coordinates  # Adiciona latitude/longitude, se disponível
                    }])
            except Exception as e:
                print(f"Failed to fetch data for city: {city} - Error: {e}")

    def get_city_and_coordinates_by_cep(self, cep):
        """Busca município e coordenadas via BrasilAPI usando o CEP."""
        if not cep:
            return "Desconhecido", None

        print(f"Fetching city and coordinates for CEP: {cep}")
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

from utils.strings import slugify
from utils.http import fetch_json
from utils.get_city_and_coords import get_city_and_coordinates_by_cep  # Importa a função isolada
from settings import BASE_URLS, MG_MUNICIPES
from states.base import BaseState

class MinasGerais(BaseState):
    def __init__(self):
        super().__init__(uf="MG", label="Minas Gerais", slug="minas-gerais")

    def fetch_data(self):

        for municipio in MG_MUNICIPES:
            print(f"Fetching data for municipio: {municipio}")

            # Fetch JSON e extrair a lista de delegacias
            response = fetch_json(f"{BASE_URLS['MG']}", {
                "municipio": municipio
            })

            if not response or "unidadesEnderecos" not in response:
                print(f"Unexpected response format for municipio {municipio}: {response}")
                continue

            unidades = response["unidadesEnderecos"].get("unidade", [])
            enderecos = response["unidadesEnderecos"].get("endereco", [])

            for unidade, endereco in zip(unidades, enderecos):
                # Identificar o município e buscar informações extras
                city, coordinates = get_city_and_coordinates_by_cep(endereco)

                # Ignorar delegacias cujo CEP não foi encontrado
                if city == "Desconhecido":
                    print(f"Skipping due to missing CEP: {endereco}")
                    continue

                # Adicionar dados agrupados por cidade
                self.add_city(slugify(city), [{
                    "name": unidade,
                    "address": endereco,
                    "coordinates": coordinates  # Adiciona latitude/longitude, se disponível
                }])

        print("Data fetching completed for Minas Gerais.")

    def get_municipios(self):
        """Retorna a lista de municípios disponíveis."""
        # Simulação de lista de municípios, deve ser implementado conforme necessário
        return ["1", "2", "3"]

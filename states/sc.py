from utils.http import fetch_html
from utils.strings import slugify
from utils.get_city_and_coords import get_city_and_coordinates_by_cep
from settings import SC_MUNICIPES, BASE_URLS
from states.base import BaseState
from bs4 import BeautifulSoup


class SantaCatarina(BaseState):
    def __init__(self):
        super().__init__(uf="SC", label="Santa Catarina", slug="santa-catarina")

    def fetch_data(self):
        """Itera pelos municípios e busca as delegacias."""
        for municipio_id, municipio_name in SC_MUNICIPES.items():
            print(f"Buscando delegacias para: {municipio_name} (ID: {municipio_id})")
            try:
                response_html = fetch_html(
                    f"{BASE_URLS['SC']}/publicacoes/pesquisa.unidades.php?pesquisa=1",
                    params={'id_unidade': municipio_id},
                    method="POST"
                )

                if not response_html:
                    print(f"Nenhuma resposta para: {municipio_name}")
                    continue

                delegacias = self.parse_response(response_html, municipio_name)
                self.add_city(slugify(municipio_name), delegacias)
            except Exception as e:
                print(f"Erro ao buscar dados para: {municipio_name} - {e}")

    def parse_response(self, html, municipio_name):
        """Processa o HTML para extrair as delegacias de um município."""
        soup = BeautifulSoup(html, 'html.parser')
        delegacias = []

        # Procurar o bloco correspondente ao município
        municipio_block = soup.find("div", class_="col-xl-6 col-lg-6 col-md-6 col-sm-6 col-6")
        if not municipio_block:
            print(f"Nenhum bloco encontrado para: {municipio_name}")
            return delegacias

        # Extrair informações das delegacias
        paragraphs = municipio_block.find_all("p")
        for p in paragraphs:
            delegacia_text = p.get_text("\n", strip=True)
            lines = delegacia_text.split("\n")
            if len(lines) < 2:
                continue  # Ignorar blocos incompletos

            name = lines[0]
            address = None
            phones = []
            email = None

            for line in lines[1:]:
                if "CEP:" in line:
                    address = line.strip()
                elif "Telefone:" in line:
                    phones.extend(line.replace("Telefone:", "").strip().split("/"))
                elif "e-mail:" in line or "emails:" in line:
                    email = line.split(":")[-1].strip()

            # Buscar cidade e coordenadas
            city, coordinates = get_city_and_coordinates_by_cep(address or "")

            delegacias.append({
                "name": name,
                "address": address,
                "phones": phones,
                "email": email,
                "coordinates": coordinates
            })

        return delegacias

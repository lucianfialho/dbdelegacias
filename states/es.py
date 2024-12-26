from bs4 import BeautifulSoup

from utils.strings import slugify
from states.base import BaseState
from settings import BASE_URLS
from utils.http import fetch_html
from utils.get_city_and_coords import get_city_and_coordinates_by_cep
class EspiritoSanto(BaseState):
    def __init__(self):
        super().__init__(uf="ES", label="Espírito Santo", slug="espirito-santo")

    def fetch_data(self):
        for url in BASE_URLS["ES"]:
            print(f"Fetching data from: {url}")
            html = fetch_html(url)

            soup = BeautifulSoup(html, 'html.parser')
            self.parse_html(soup)

        print("Data fetching completed for Espírito Santo.")

    def parse_html(self, soup):
        tables = soup.find_all("table")
        
        for table in tables:
            rows = table.find_all("tr")
            for row in rows[2:]:  # Skip header rows
                cells = row.find_all("td")
                if len(cells) < 4:
                    continue

                name = cells[0].get_text(strip=True)
                hours = cells[1].get_text(strip=True)
                phone = cells[2].get_text(strip=True).replace("\n", " ")
                address_elements = cells[3].select("h6")
                address = ' '.join(elem.get_text(strip=True) for elem in address_elements)

                # Extract city from address (assumes city is the last line before "CEP")
                localInfo = get_city_and_coordinates_by_cep(address)
                print(localInfo)
                city = localInfo[0]  # Extract city name from tuple
                # Add data grouped by city
                self.add_city(slugify(city), [{
                    "name": name,
                    "address": address,
                    "phone": phone,
                    "hours": hours,
                    "coordinates": localInfo[1]
                }])

    def get_city(self, address):
        if "CEP" in address:
            parts = address.split("CEP")
            city_line = parts[0].strip().split(",")[-1].strip()
            return city_line
        return "Desconhecido"

# Example usage
if __name__ == "__main__":
    es = EspiritoSanto()
    es.fetch_data()

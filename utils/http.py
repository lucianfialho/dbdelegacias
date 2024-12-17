import requests

def fetch_json(url, params=None):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Levanta um erro para códigos de status HTTP >= 400
        data = response.json()  # Retorna o JSON convertido
        return data
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer requisição para {url}: {e}")
        return None

def fetch_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

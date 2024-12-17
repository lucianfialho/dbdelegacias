import requests

def fetch_json(url, params=None):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer requisição para {url}: {e}")
        return None

def fetch_html(url, params=None, method="GET", headers=None):
    try:
        if method == "POST":
            response = requests.post(url, data=params, headers=headers)
        else:
            response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer requisição para {url}: {e}")
        return None

import requests

def fetch_json(url, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def fetch_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

from bs4 import BeautifulSoup

def parse_table(html, selector):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.select(selector)
    return table

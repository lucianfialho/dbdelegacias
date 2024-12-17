import re
import unicodedata

def slugify(value):
    """Converte uma string em um slug formatado."""
    value = unicodedata.normalize("NFKD", value).encode("ASCII", "ignore").decode("utf-8")
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value

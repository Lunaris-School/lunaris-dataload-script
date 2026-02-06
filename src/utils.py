import re
import unicodedata

def clean_string(text):
    """Remove acentos e caracteres especiais."""
    nfkd_form = unicodedata.normalize('NFKD', text)
    text = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    text = text.lower().strip()
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', '.', text)
    return text

def format_email(name, domain="lunaris.org.br"):
    return f"{clean_string(name)}@{domain}"
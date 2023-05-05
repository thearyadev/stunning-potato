from bs4 import BeautifulSoup
import requests

def get_document(url: str):
    """Get document from url"""
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")
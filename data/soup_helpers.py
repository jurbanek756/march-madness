from bs4 import BeautifulSoup
import requests


def get_table(url, table_index=0):
    data = requests.get(url).content
    souper = BeautifulSoup(data, "html.parser")
    return souper.find_all("table")[table_index]

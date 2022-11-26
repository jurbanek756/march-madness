"""
Helper module for common BeautifulSoup operations
"""

from bs4 import BeautifulSoup
import requests


def get_table(url, table_index=0):
    """
    Gets a table from a URL at a specified index

    Parameters
    ----------
    url: str
    table_index: int

    Returns
    -------
    BeautifulSoup
    """
    data = requests.get(url).content
    souper = BeautifulSoup(data, "html.parser")
    return souper.find_all("table")[table_index]

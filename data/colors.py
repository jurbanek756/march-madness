"""
Module for gathering and parsing data on school colors
"""

from bs4 import BeautifulSoup
import requests
import webcolors

from helpers.soup_helpers import get_table


def get_all_school_colors():
    """
    Gets school primary and secondary colors from an external source

    Returns
    -------
    list of tuple
        school, primary color, secondary color
    """
    data = requests.get("https://www.caninejournal.com/college-colors/")
    b = BeautifulSoup(data.text, "html.parser")
    line_break_set = {
        "Name",
        "City",
        "Mascot",
        "Nickname",
        "Location",
        "Team Name",
        "Home of the Catamounts",
        "The Island University",
        "Marching Highland Cavaliers",
        "Senators",
    }
    color_data = list()
    for line in b.find_all("li")[46:]:
        if line and ":" in line.text:
            sp = line.text.split(":")
            school = sp[0].strip()
            colors = sp[1]
            for t in line_break_set:
                colors = colors.split(t)[0].strip()
            if "&" in colors:
                color_split = colors.split("&")
                primary_color = color_split[0].strip()
                secondary_color = color_split[1].strip()
            elif "," in colors:
                color_split = colors.split(",")
                primary_color = color_split[0].strip()
                secondary_color = color_split[1].split("&")[0].strip()
            else:
                continue
            if school and school not in line_break_set:
                color_data.append((school, primary_color, secondary_color))
    return color_data


def school_colors_dict():
    return {
        "Creighton": ("blue", "white"),
        "TCU": ("purple", "white"),
        "UCLA": ("blue", "gold"),
        "Gonzaga": ("white", "navy"),
        "St. Mary's": ("white", "blue"),
        "UT Arlington": ("black", "blue"),
        "Xavier": ("white", "silver"),
        "Hawaii": ("white", "green"),
        "UNLV": ("gray", "red"),
        "Drexel": ("blue", "gold")
    }

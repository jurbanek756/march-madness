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
            if "," in colors:
                color_split = colors.split(",")
                primary_color = color_split[0].strip()
                secondary_color = color_split[1].split("&")[0].strip()
            if school and school not in line_break_set:
                color_data.append((school, primary_color, secondary_color))
    return color_data


def closest_colour(requested_hex):
    """
    Converts a hex color to a readable name

    References
    ----------
    https://stackoverflow.com/questions/9694165/convert-rgb-color-to-english-color-name-like-green-with-python

    Parameters
    ----------
    requested_hex: str

    Returns
    -------

    """
    min_colours = {}
    requested_rgb = webcolors.hex_to_rgb(requested_hex)
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_rgb[0]) ** 2
        gd = (g_c - requested_rgb[1]) ** 2
        bd = (b_c - requested_rgb[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def get_color_name(hex_color):
    """
    Gets a color name from a hex color value

    Parameters
    ----------
    hex_color: str

    Returns
    -------
    str
    """
    try:
        return webcolors.hex_to_name(hex_color)
    except ValueError:
        return closest_colour(hex_color)


def get_all_school_colors_from_mascot_names():
    """
    Gets all school colors from a table that correlates hex color codes with school mascot names. This table is
    not currently used, as it is more difficult to correlate a school's nickname and mascot with their formal name
    used in the main dataframe.

    Returns
    -------
    list of tuple
        school, primary color, secondary color
    """
    color_table = get_table("https://en.wikipedia.org/wiki/Module:College_color", 3)
    colors = list()
    for i, row in enumerate(color_table.find_all("tr")[2:]):
        cdata = row.find_all("td")
        name = cdata[0].string
        color1 = cdata[1].get("style").split(":")[1]
        color2 = cdata[3].get("style").split(":")[1]
        if "transparent" in color2:
            color2 = cdata[2].get("style").split(":")[1]
        if name:
            colors.append((name, get_color_name(color1), get_color_name(color2)))
    return colors


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
        "UNLV": ("gray", "red")
    }

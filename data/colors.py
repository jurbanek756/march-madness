"""
Module for gathering and parsing data on school colors
"""

from data.espn import get_teams_from_api
import webcolors


def get_all_school_colors():
    teams = get_teams_from_api()
    colors_dict = dict()
    for team in teams:
        colors_dict[team["shortDisplayName"]] = {
            "primary_color": get_color_name(team["color"]),
            "secondary_color": get_color_name(team.get("alternateColor")),
        }
    return colors_dict


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
    requested_rgb = webcolors.hex_to_rgb(f"#{requested_hex}")
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
    if not hex_color:
        return None
    try:
        return webcolors.hex_to_name(hex_color)
    except ValueError:
        return closest_colour(hex_color)

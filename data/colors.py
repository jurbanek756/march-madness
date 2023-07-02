"""
Module for gathering and parsing data on school colors
"""

from data.espn import get_teams_from_api, get_name
from models.colors import Colors
import webcolors


def get_all_school_colors():
    teams = get_teams_from_api()
    colors_dict = dict()
    for team in teams:
        team_name = get_name(team["shortDisplayName"])
        colors_dict[team_name] = {
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
    Gets a color name from a hex color value, then further simplifies it using
    COLOR_DICT

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
        color = webcolors.hex_to_name(hex_color)
    except ValueError:
        color = closest_colour(hex_color)
    try:
        return COLOR_DICT[color]
    except KeyError:
        raise ValueError(f"Color {color} not found in COLOR_DICT")


COLOR_DICT = {
    "midnightblue": Colors.NAVY,
    "darkcyan": Colors.TEAL,
    "darkolivegreen": Colors.GREEN,
    "deepskyblue": Colors.LIGHT_BLUE,
    "mediumturquoise": Colors.LIGHT_BLUE,
    "darkslateblue": Colors.PURPLE,
    "darkgoldenrod": Colors.GOLD,
    "darkslategray": Colors.GRAY,
    "olive": Colors.GREEN,
    "darkgray": Colors.GRAY,
    "saddlebrown": Colors.BROWN,
    "darkblue": Colors.NAVY,
    "sienna": Colors.BROWN,
    "darksalmon": Colors.ORANGE,
    "cornflowerblue": Colors.LIGHT_BLUE,
    "limegreen": Colors.GREEN,
    "tomato": Colors.RED,
    "firebrick": Colors.RED,
    "mediumblue": Colors.BLUE,
    "skyblue": Colors.LIGHT_BLUE,
    "lavender": Colors.PURPLE,
    "indigo": Colors.PURPLE,
    "palegoldenrod": Colors.GOLD,
    "tan": Colors.BROWN,
    "lightslategray": Colors.GRAY,
    "brown": Colors.BROWN,
    "linen": Colors.WHITE,
    "white": Colors.WHITE,
    "peru": Colors.BROWN,
    "darkkhaki": Colors.BROWN,
    "sandybrown": Colors.ORANGE,
    "gold": Colors.GOLD,
    "red": Colors.RED,
    "forestgreen": Colors.GREEN,
    "seagreen": Colors.GREEN,
    "black": Colors.BLACK,
    "whitesmoke": Colors.WHITE,
    "gray": Colors.GRAY,
    "orangered": Colors.ORANGE,
    "gainsboro": Colors.GRAY,
    "chocolate": Colors.BROWN,
    "dodgerblue": Colors.BLUE,
    "crimson": Colors.RED,
    "goldenrod": Colors.GOLD,
    "cadetblue": Colors.BLUE,
    "maroon": Colors.RED,
    "teal": Colors.TEAL,
    "dimgray": Colors.GRAY,
    "darkgreen": Colors.GREEN,
    "purple": Colors.PURPLE,
    "orange": Colors.ORANGE,
    "silver": Colors.GRAY,
    "navy": Colors.NAVY,
    "darkorange": Colors.ORANGE,
    "lightblue": Colors.LIGHT_BLUE,
    "khaki": Colors.BROWN,
    "wheat": Colors.BROWN,
    "darkred": Colors.RED,
    "rosybrown": Colors.BROWN,
    "coral": Colors.ORANGE,
    "burlywood": Colors.BROWN,
    "steelblue": Colors.BLUE,
    "lightgray": Colors.GRAY,
}

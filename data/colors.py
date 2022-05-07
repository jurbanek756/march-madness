import webcolors

from data.soup_helpers import get_table


def closest_colour(requested_hex):
    """
    Adapted from:
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
    try:
        return webcolors.hex_to_name(hex_color)
    except ValueError:
        return closest_colour(hex_color)


def get_all_school_colors():
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



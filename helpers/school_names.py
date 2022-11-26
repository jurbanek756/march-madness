"""
Module for parsing school names
"""

from us import states



SPECIAL_CASES = {
    "UConn": "University of Connecticut",
    "Illinois": "University of Illinois Urbana-Champaign",
    "Texas": "University of Texas at Austin",
}
STATES = [str(s) for s in states.STATES]


def update_school_name(school_name):
    """
    Updates a school name from its common abbreviation to its more formalized version. Also prunes parentheses.

    Parameters
    ----------
    school_name: str

    Returns
    -------
    str
    """
    if school_name[-1] == ")" and school_name[-4] == "(":
        school_name = school_name[:-5]
    elif school_name[-1] == ")" and school_name[-3] == "(":
        school_name = school_name[:-4]
    if school_name in SPECIAL_CASES:
        school_name = SPECIAL_CASES[school_name]
    elif school_name in STATES:
        school_name = f"University of {school_name}"
    return school_name

from itertools import zip_longest


def print_in_two_columns(s1_obj, s2_obj, col_size=45):
    """

    Parameters
    ----------
    s1_obj
    s2_obj
    col_size

    References
    ----------
    https://stackoverflow.com/a/53401505/8728749

    Returns
    -------

    """
    if isinstance(s1_obj, str):
        s1_obj = [s1_obj]
    if isinstance(s2_obj, str):
        s2_obj = [s2_obj]
    for s1, s2 in zip_longest(s1_obj.game_results, s2_obj.game_results):
        print(s1[:col_size].ljust(col_size) + "    " + s2[:col_size])

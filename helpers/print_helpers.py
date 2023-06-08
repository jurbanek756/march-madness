from itertools import zip_longest


def print_in_two_columns(s1_obj, s2_obj, s1_header=None, s2_header=None, col_size=45):
    """

    Parameters
    ----------
    s1_obj
    s2_obj
    s1_header
    s2_header
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
    if s1_header or s2_header:
        print(s1_header[:col_size].ljust(col_size) + "    " + s2_header[:col_size])
        print("-" * col_size + "    " + "-" * col_size)
    for s1, s2 in zip_longest(s1_obj, s2_obj):
        if not s1:
            s1 = ""
        if not s2:
            s2 = ""
        print(s1[:col_size].ljust(col_size) + "    " + s2[:col_size])

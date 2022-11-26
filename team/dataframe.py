"""
Module for adding relevant data to a DataFrame
"""

from data.colors import get_all_school_colors
from data.location import create_location_status_tuple
from data.rivals import RIVALRIES
from helpers.school_names import update_school_name
from helpers.soup_helpers import get_table
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import pandas as pd
import requests

WIKIPEDIA = "https://en.wikipedia.org/wiki"
D1_BASKETBALL_SCHOOLS = f"{WIKIPEDIA}/List_of_NCAA_Division_I_men%27s_basketball_programs"
DI_SCHOOLS = f"{WIKIPEDIA}/List_of_NCAA_Division_I_institutions"
AP_RANKINGS = "https://www.ncaa.com/rankings/basketball-men/d1/associated-press"


def get_all_d1_schools():
    table = get_table(D1_BASKETBALL_SCHOOLS)
    columns = [c.string.strip() for c in table.find_all("th")]
    additional_rows = ["AP Ranking", "Tournament Ranking"]
    for r in additional_rows:
        columns.append(r)
    all_school_data = list()
    for school in table.find_all("tr")[1:]:
        school_data = list()
        for d in school.find_all("td"):
            content = d.string
            if not content:
                content = d.find("a").text
            content = content.strip()
            school_data.append(content)
        for _ in additional_rows:
            school_data.append(None)
        all_school_data.append(school_data)
    return pd.DataFrame(all_school_data, columns=columns)


def add_ap_rankings_to_dataframe(df):
    data = requests.get(AP_RANKINGS).content
    ap_ranks = BeautifulSoup(data, "html.parser")
    tuple_list = list()
    for d in ap_ranks.find("table").find_all("tr")[1:]:
        td = d.find_all("td")
        tuple_list.append((td[1].string, td[0].string))
    return add_data_to_dataframe(df, tuple_list, "AP Ranking")


def add_tournament_rankings_to_dataframe_from_csv(df, filename):
    tuple_list = list()
    with open(filename, "r") as F:
        for line in F:
            content = line.split(",")
            tuple_list.append((update_school_name(",".join(content[0:-1])), content[-1]))
    return add_data_to_dataframe(df, tuple_list, "Tournament Ranking")


def add_team_colors_to_dataframe(df):
    data = get_all_school_colors()
    for i, row in df.iterrows():
        best_index, best_ratio = school_index_in_tuple(row["School"], data)
        if best_ratio > 95:
            df.at[i, "Primary Color"] = data[best_index][1]
            df.at[i, "Secondary Color"] = data[best_index][2]


def add_location_and_is_private_to_dataframe(df):
    data = create_location_status_tuple()
    for i, row in df.iterrows():
        best_index, best_ratio = school_index_in_tuple(row["School"], data)
        if best_ratio > 95:
            df.at[i, "Location"] = data[best_index][1]
            df.at[i, "Is Private"] = data[best_index][2]


def add_rivals_to_dataframe(df):
    df["Rivals"] = df["School"].map(RIVALRIES)


def school_index_in_tuple(df_school, data):
    best_ratio = 0
    best_index = -1
    for j, (school, _, _) in enumerate(data):
        ap_name = update_school_name(school)
        for q, r in [("St.", "Saint"), ("The ", "")]:
            ap_name.replace(q, r)
            df_school.replace(q, r)
        split_ap_name = ap_name.casefold().split(" ")
        split_df_school = df_school.casefold().split(" ")
        generic = "University"
        if split_ap_name[-1] == generic.casefold() and split_df_school[-1] == generic.casefold():
            ratio = fuzz.ratio(" ".join(split_df_school[:-1]), " ".join(split_ap_name[:-1]))
        elif split_ap_name[0] == generic.casefold() and split_df_school[0] == generic.casefold():
            ratio = fuzz.ratio(" ".join(split_df_school[1:]), " ".join(split_ap_name[1:]))
        else:
            ratio = fuzz.ratio(df_school, ap_name)
        if ratio > best_ratio:
            best_ratio = ratio
            best_index = j
    return best_index, best_ratio


def filter_none_values(df, attribute):
    return df[df[attribute].notnull()]


def add_data_to_dataframe(df, data_tuple_list, attribute):
    """

    Parameters
    ----------
    df: DataFrame
    data_tuple_list: tuple
        Form is (school, value of attribute)
    attribute: str
        Attribute being updated

    Returns
    -------
    DataFrame
    """
    for d in data_tuple_list:
        best_ratio = 0
        best_index = -1
        for i, row in df.iterrows():
            ap_name = update_school_name(d[0])
            ratio = fuzz.ratio(row["School"], ap_name)
            if ratio > best_ratio:
                best_ratio = ratio
                best_index = i
        df.at[best_index, attribute] = int(d[1])
    return df

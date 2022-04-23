#!/usr/bin/env python

from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import pandas as pd
import requests
from us import states

D1_SCHOOLS = "https://en.wikipedia.org/wiki/List_of_NCAA_Division_I_men%27s_basketball_programs"
AP_RANKINGS = "https://www.ncaa.com/rankings/basketball-men/d1/associated-press"
STATES = [str(s) for s in states.STATES]
SPECIAL_CASES = {
    "UConn": "University of Connecticut",
    "Illinois": "University of Illinois Urbana-Champaign",
    "Texas": "University of Texas Austin",
}


def get_all_d1_schools():
    data = requests.get(D1_SCHOOLS).content
    souper = BeautifulSoup(data, "html.parser")
    table = souper.find("table")
    columns = [c.string.strip() for c in table.find_all("th")]
    columns.append("AP Ranking")
    all_school_data = list()
    for school in table.find_all("tr")[1:]:
        school_data = list()
        for d in school.find_all("td"):
            content = d.string
            if not content:
                content = d.find("a").text
            content = content.strip()
            school_data.append(content)
        school_data.append(None)
        all_school_data.append(school_data)
    return pd.DataFrame(all_school_data, columns=columns)


def add_ap_rankings_to_dataframe(df):
    data = requests.get(AP_RANKINGS).content
    ap_ranks = BeautifulSoup(data, "html.parser")
    for d in ap_ranks.find("table").find_all("tr")[1:]:
        td = d.find_all("td")
        best_ratio = 0
        best_index = -1
        for i, row in df.iterrows():
            ap_name = td[1].string
            if ap_name[-1] == ")" and ap_name[-4] == "(":
                ap_name = ap_name[:-5]
            elif ap_name[-1] == ")" and ap_name[-3] == "(":
                ap_name = ap_name[:-4]
            if ap_name in SPECIAL_CASES:
                ap_name = SPECIAL_CASES[ap_name]
            elif ap_name in STATES:
                ap_name = f"University of {ap_name}"
            ratio = fuzz.ratio(row["School"], ap_name)
            if ratio > best_ratio:
                best_ratio = ratio
                best_index = i
        df.at[best_index, "AP Ranking"] = int(td[0].string)
    return df

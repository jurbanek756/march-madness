import pickle
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mmsite.settings")
import django

django.setup()
from marchmadness.models import School

from math import isnan
import sys

sys.path.append("../")


def get_parens_num(prov_str):
    return int(prov_str.split(")")[0].split("(")[1])


def insert_bool(val):
    if isnan(val):
        return False
    return val


with open("../db/school_data.pkl", "rb") as F:
    df = pickle.load(F)

schools_to_insert = []
for i, row in df.iterrows():
    school = School(
        name=row["Name"],
        formal_name=row["School"],
        nickname=row["Nickname"],
        home_arena=row["Home arena"],
        conference=row["Conference"],
        tournament_appearances=get_parens_num(row["Tournament appearances"]),
        final_four_appearances=get_parens_num(row["Final Four appearances"]),
        championship_wins=get_parens_num(row["Championship wins"]),
        primary_color=row["Primary Color"],
        secondary_color=row["Secondary Color"],
        location=row["Location"],
        is_private=insert_bool(row["Is Private"]),
    )
    schools_to_insert.append(school)

School.objects.bulk_create(schools_to_insert)

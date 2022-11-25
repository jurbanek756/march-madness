from data.soup_helpers import get_table

WIKIPEDIA = "https://en.wikipedia.org/wiki"
DI_SCHOOLS = f"{WIKIPEDIA}/List_of_NCAA_Division_I_institutions"


def create_location_status_tuple():
    schools_table = get_table(DI_SCHOOLS, 1)
    school_data = list()
    for row in schools_table.find_all("tr")[2:]:
        data = row.find_all("td")
        school = data[0].find("a").text
        location = f"{data[3].find('a').text}, {data[4].find('a').text}"
        is_private = data[5].find("a").text.casefold() == "private".casefold()
        school_data.append((school, location, is_private))
    return school_data

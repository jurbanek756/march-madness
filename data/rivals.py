"""
Sources:
- https://bleacherreport.com/articles/1719358-ranking-the-25-best-rivalries-in-college-basketball
"""

RIVALRIES = {
    "Duke University": "University of North Carolina",
    "University of Michigan": "Ohio State University",
    "University of Kentucky": "University of Louisville",
    "University of Cincinnati": "Xavier University",
    "Indiana University Bloomington": "Purdue University",
    "Gonzaga University": "Saint Mary's College of California",
    "University of Kansas": "Kansas State University",
    "University of Michigan": "Michigan State University",
    "University of Pennsylvania": "Princeton University",
    "Harvard University": "Yale University",
    "University of Arkansas": "University of Missouri",
    "Syracuse University": "University of Pittsburgh",
    "Marquette University": "University of Notre Dame",
    "University of Iowa": "Iowa State University",
    "Stanford University": "University of California, Berkeley",
    "University of Illinois Urbana–Champaign": "University of Missouri",
    "Marquette University": "University of Wisconsin–Madison",
    "Villanova University": "LaSalle University",
    "University of Connecticut": "Syracuse University",
    "Indiana University Bloomington": "University of Kentucky",
    "Duke University": "University of Maryland, College Park",
    "Syracuse University": "Georgetown University",
    "University of Kentucky": "University of Florida",
    "Georgetown University": "Villanova University",
    "University of California, Los Angeles": "University of Arizona"
}
RIVALRIES = RIVALRIES | {v: k for k, v in RIVALRIES.items()}

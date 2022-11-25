"""
Sources:
- https://bleacherreport.com/articles/1719358-ranking-the-25-best-rivalries-in-college-basketball
"""

RIVALRIES = {
    "Duke University": "University of North Carolina",
    "University of Michiagan": "Ohio State University",
    "University of Kentucky": "University of Louisville",
    "University of Cincannati": "Xavier University",
    "Indiana University": "Purdue University",
    "Gonzaga University": "St. Mary's University",
    "University of Kansas": "Kansas State University",
    "University of Michigan": "Michigan State University",
    "University of Pennsylvania": "Princeton University",
    "Harvard University": "Yale University",
    "University of Arkansas": "University of Missouri",
    "Syracuse University": "University of Pittsburgh",
    "Marquette University": "University of Notre Dame",
    "University of Iowa": "Iowa State University",
    "Stanford University": "University of California-Berkeley",
    "University of Illinois-Urbana-Champagin": "University of Missouri",
    "Marquette University": "University of Wisconsin",
    "Villanova University": "LaSalle University",
    "University of Connecticut": "Syracuse University",
    "Indiana University": "University of Kentucky",
    "Duke University": "University of Maryland",
    "Syracuse University": "Georgetown University",
    "University of Kentucky": "University of Florida",
    "Georgetown University": "Villanova University",
    "University of California-Los Angeles": "Unversity of Arizona"
}
RIVALRIES = RIVALRIES | {v: k for k, v in RIVALRIES.items()}

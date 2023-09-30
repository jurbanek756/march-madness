# Django setup to use models
import sys
import os
sys.path.append("mmsite/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mmsite.settings")
import django

django.setup()

from marchmadness.models import School, Game, APRanking, TournamentRanking


all_schools = School.objects.all()
teams_in_tournamnent = TournamentRanking.objects.filter(year=2023)
breakpoint()
from django.core.management.base import BaseCommand, CommandError
import datetime
import requests
import csv
import re
from bs4 import BeautifulSoup
from gdanalyst.models import School, City
from progress.bar import Bar

class Command(BaseCommand):
    help = 'Updates the City model with locations'

    def handle(self, *args, **options):
        teams = School.objects.filter(world="heisman").all()
        team_info_URL = f"https://www.whatifsports.com/gd/TeamProfile/PlayerRatings.aspx?tid="
        team_info = []
        self.stdout.write(f"Starting to download school info . . . ({datetime.datetime.now()})")

        with Bar('Uploading Schools', max=len(teams)) as bar:
            for t in teams:
                team_info_page = requests.get(team_info_URL + str(t.wis_id))
                soup = BeautifulSoup(team_info_page.content, 'html.parser')
                teamInfoBar = soup.find(class_="teamInfoBar")
                t_info = re.search(r'([a-zA-z0-9-]*)\nConference: ([a-zA-z0-9- ]*)\nCoach: ([a-zA-z0-9- ]*)', teamInfoBar.text)
                try:
                    record = t_info.group(1)
                except:
                    record = ""
                conference = t_info.group(2)
                coach = t_info.group(3)
                teamDivision = soup.find(id="ctl00_ctl00_ctl00_Main_Main_spnDivision")
                teamLocation = soup.find(id="ctl00_ctl00_ctl00_Main_Main_spnLocation")
                tmp = [t.wis_id, record, conference, coach, teamDivision.text, teamLocation.text]
                team_info.append(tmp)
                bar.next()

        self.stdout.write(f"Finished downloading team info . . . ({datetime.datetime.now()})")

        with open('school_download_info.csv', 'w', newline='') as writerfile:
            writer = csv.writer(writerfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['wisid','record', 'conference', 'coach', 'division', 'location'])
            for row in team_info:
                print(row)
                writer.writerow(row)
        return
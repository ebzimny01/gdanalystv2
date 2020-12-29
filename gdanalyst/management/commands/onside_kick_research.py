from django.core.management.base import BaseCommand, CommandError
import datetime
import requests
import csv
import re
from bs4 import BeautifulSoup
from gdanalyst.models import School, City
from progress.bar import Bar
from gdanalyst.views import get_schedule_table

class Command(BaseCommand):
    help = 'Used to research how many times onside kicks are recovered by kicking team'

    def handle(self, *args, **options):
        world = "wilkinson"
        teams = School.objects.filter(world=f"{world}").all()
        team_info_URL = f"https://www.whatifsports.com/gd/TeamProfile/PlayerRatings.aspx?tid="
        world_game_IDs = set()
        
        self.stdout.write(f"Starting to download game IDs for each school in {world} . . . ({datetime.datetime.now()})")

        with Bar(f'Grabbing Game IDs for each school in {world}', max=len(teams)) as bar:
            for t in teams:
                temp = get_schedule_table(t.wis_id)
                for each in temp:
                    if re.match(r'[\d]{7}', each[6]):         
                        world_game_IDs.add(each[6])
                # breakpoint()
                bar.next()

        self.stdout.write(f"Finished downloading game IDs for {world} . . . ({datetime.datetime.now()})")

        with open('gameid.csv', 'w', newline='') as writerfile:
            writer = csv.writer(writerfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['gid'])
            for row in world_game_IDs:
                print(row)
                writer.writerow(row)

        pbp_baseURL = "https://www.whatifsports.com/gd/GameResults/PlayByPlay.aspx?gid="
        pbp_q_suffix = "&quarter=4"
        onside_kick_results = []
        
        self.stdout.write(f"Starting to grab onside kick results for {world} . . . ({datetime.datetime.now()})")
        with Bar(f'Finding onside kick results for {len(world_game_IDs)} game IDs . . . ', max=len(world_game_IDs)) as bar:
            for gid in world_game_IDs:
                pbpURL = pbp_baseURL + str(gid) + pbp_q_suffix
                # print(pbpURL)
                pbprawpage = requests.get(pbpURL)
                soup = BeautifulSoup(pbprawpage.content, 'html.parser')
                pbp_desc = soup.find_all(string=re.compile(r"onside kick from the .*i?s? recovered at the .* by the (.*ing) team."))
                if len(pbp_desc) > 0:
                    for i in pbp_desc:
                        onside_kick_results.append([gid,i])
                bar.next()

        self.stdout.write(f"Finished grabbing onside kick results for {world} . . . ({datetime.datetime.now()})")

        with open('onside.csv', 'w', newline='') as writerfile:
            writer = csv.writer(writerfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['gid','onside_text'])
            for row in onside_kick_results:
                print(row)
                writer.writerow(row)
                
        return
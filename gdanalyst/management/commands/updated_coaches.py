from django.core.management.base import BaseCommand, CommandError
import requests, urllib.parse, datetime
from bs4 import BeautifulSoup
from gdanalyst.models import School, City
from progress.bar import Bar

class Command(BaseCommand):
    help = 'Updates the coaches of each school across all worlds'

    def handle(self, *args, **options):
        self.stdout.write(f"Starting to update coaches . . . ({datetime.datetime.now()})")
        try:
            # coaches = School.objects.all()
            coaches = School.objects.filter(world="yost").all()
        except School.DoesNotExist:
            raise CommandError('Error accessing School model data')
        baseURL = 'https://www.whatifsports.com/gd/TeamProfile/PlayerRatings.aspx?tid='
        coach_total = len(coaches)
        with Bar('Updating coaches', max=coach_total) as bar:
            for coach in coaches:
                teamURL = baseURL + str(coach.wis_id)
                try:
                    teampage = requests.get(teamURL)
                    teampage.raise_for_status()
                except requests.exceptions.HTTPError as errh:
                    raise CommandError("Http Error:",errh)
                except requests.exceptions.ConnectionError as errc:
                    raise CommandError("Error Connecting:",errc)
                except requests.exceptions.Timeout as errt:
                    raise CommandError("Timeout Error:",errt)
                except requests.exceptions.RequestException as err:
                    raise CommandError("OOps: Something Else",err)
                soup = BeautifulSoup(teampage.content, 'html.parser')
                headcoach = soup.find(class_="coachProfileLink")
                # self.stdout.write(headcoach.text)
                if headcoach.text != coach.coach:
                    coach.coach = headcoach.text
                    coach.save()
                bar.next()
        self.stdout.write(f"Finished updating coaches . . . ({datetime.datetime.now()})")
        return
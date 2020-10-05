from django.core.management.base import BaseCommand, CommandError
import datetime
import urllib.request
import csv
from gdanalyst.models import School, City
from progress.bar import Bar

class Command(BaseCommand):
    help = 'Updates the City model with locations'

    def handle(self, *args, **options):
        url = "https://ez-gdapp.s3.amazonaws.com/school_table.csv"
        response = urllib.request.urlopen(url)
        lines = [l.decode('utf-8') for l in response.readlines()]
        reader = csv.reader(lines)
        print(reader)
        next(reader)
        self.stdout.write(f"Starting to upload schools . . . ({datetime.datetime.now()})")
        with Bar('Uploading Schools', max=len(lines)) as bar:
            for row in reader:
                school = School.objects.get(wis_id = row[0])
                # school.school_long = row[1]
                # school.school_short = row[2]
                # school.world = row[3]
                # school.location = City.objects.get(id=row[4])
                school.division = row[5]
                school.conference = row[6]
                # school.coach = "Sim AI"
                school.save()
                bar.next()
        self.stdout.write(f"Finished updating cities . . . ({datetime.datetime.now()})")
        return
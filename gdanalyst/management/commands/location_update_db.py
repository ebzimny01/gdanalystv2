from django.core.management.base import BaseCommand, CommandError
import datetime
import urllib.request
import csv
from gdanalyst.models import School, City
from progress.bar import Bar

class Command(BaseCommand):
    help = 'Updates the City model with locations'

    def handle(self, *args, **options):
        url = "https://ez-gdapp.s3.amazonaws.com/gd_locations.csv"
        response = urllib.request.urlopen(url)
        lines = [l.decode('utf-8') for l in response.readlines()]
        reader = csv.reader(lines)
        print(reader)
        next(reader)
        self.stdout.write(f"Starting to update locations . . . ({datetime.datetime.now()})")

        with Bar('Updating cities', max=len(lines)) as bar:
            for row in reader:
                city = City()
                city.name = row[2]
                city.latitude = row[3]
                city.longitude = row[4]
                city.school_long = row[1]
                print(city)
                city.save()
                bar.next()
        self.stdout.write(f"Finished updating cities . . . ({datetime.datetime.now()})")
        return
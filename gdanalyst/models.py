from django.db import models

# Create your models here.

class City (models.Model):
    name = models.CharField(max_length=64, default="blank")
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    school_long = models.CharField(max_length=64, default="blank")

    def __str__(self):
        return f"{self.name} Lat={self.latitude} Lon={self.longitude}"

class School (models.Model):
    wis_id = models.PositiveIntegerField(unique=True)
    school_long = models.CharField(max_length=64)
    school_short = models.CharField(max_length=40)
    world = models.CharField(max_length=15)
    location = models.ForeignKey(City, on_delete=models.CASCADE, related_name="collegetown")
    division = models.CharField(max_length=8, blank=True)
    conference = models.CharField(max_length=64, blank=True)
    coach = models.CharField(max_length=64, default="Sim AI")

    def __str__(self):
        return f"{self.school_short} ({self.wis_id})"
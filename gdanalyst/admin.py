from django.contrib import admin

# Register your models here.

from .models import School, City

class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "latitude", "longitude", "school_long")

class SchoolAdmin(admin.ModelAdmin):
    list_display = ("id", "wis_id", "school_long", "school_short", "world", "location", "division", "conference", "coach")

admin.site.register(School, SchoolAdmin)
admin.site.register(City, CityAdmin)
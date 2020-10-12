from django.urls import path

from . import views

urlpatterns = [
    # path("map", views.map, name="map"), # no longer used
    path("", views.index, name="index"),
    path("schools", views.schools, name="schools"),
    path("<int:wisid>", views.wisid, name="wisid"),
    path("<int:wisid>/schedule", views.teamschedule, name="teamschedule"),
    path("world/<str:worldname>", views.world, name="world"),
    path("world/<str:worldname>/<str:division>", views.division, name="division"),
    path("location/<int:wisid>", views.location, name="location"),
    path("world/<str:worldname>/<str:division>/player", views.player, name="player"),
    path("gameid", views.gameid, name="gameid"),
    path("pbp", views.pbp, name="pbp"),
    path("<int:wisid>/schedule/all", views.get_all_results, name="get_all_results"),
    path("<int:wisid>/schedule/humans", views.get_all_results, name="get_all_results"),
    path("coach/<str:coachid>", views.coach, name="coach")
]
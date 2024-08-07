import requests
import django_rq
from django.urls import reverse
from urllib.parse import urlencode
from requests.api import head
from rq.job import Job
from django_redis import get_redis_connection
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.html import escape
from django.views.decorators.http import require_GET
from bs4 import BeautifulSoup
from django import forms
from math import radians, cos, sin, asin, sqrt 
from .models import School, City
from .playbyplay import *
from .utils import total_size

# Create your views here.

class SelectSchoolForm(forms.Form):
    world = forms.ModelChoiceField(label="World", queryset=School.objects.values_list('world').order_by('world').distinct())

def index(request):
    selectschool = SelectSchoolForm()
    return render(request, "gdanalyst/index.html", {
            "form": selectschool
        })


@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /*",
        "Disallow: /world/*/*/player",
        "Disallow: /world/*/*/town",
        "Disallow: /schools",
        "Disallow: /pbp*",
        "Disallow: /loadinggameresults*"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def schools(request):
    w = request.GET['Worlds']
    d = request.GET['Divisions']
    school_list = School.objects.filter(world=w).filter(division=d).order_by('school_short').all()
    school_list_hct = school_list.exclude(coach="Sim AI").all()
    return render(request, "gdanalyst/division.html", {
        "world": w,
        "division": d,
        "schools": school_list,
        "coachcount": len(school_list_hct)
    })

def wisid(request, wisid):
    wid = School.objects.get(wis_id=wisid)
    coach = wid.coach
    # get team roster and position counts
    roster = teamroster(wisid)
    # 'hct' stands for human coached teams
    hct = School.objects.exclude(coach="Sim AI").filter(world=wid.world).filter(division=wid.division)
    teamdistance = get_distance(wid.location, hct)
    combined = {}
    for each in hct:
        combined[each.wis_id] = [each.school_short, each.coach, teamdistance[each.wis_id], each.location.latitude, each.location.longitude]
    K = 2
    combined_sorted = sorted(combined.items(), key=lambda x: x[1][K])
    return render(request, "gdanalyst/wisid.html", {
        "wid": wid,
        "coach": coach,
        "roster": roster,
        "hct": hct,
        "coachcount": len(hct),
        "distance": teamdistance.values,
        "combined": combined_sorted
    })

def location(request, wisid):
    school = School.objects.get(wis_id=wisid)
    coach = school.coach
    data = [school.location.latitude, school.location.longitude, school.school_short, coach]
    return JsonResponse(data, safe=False)

def world(request, worldname):
    return render(request, "gdanalyst/world.html", {
        "world": worldname
    })

def division(request, worldname, division):
    school_list = School.objects.filter(world=worldname).filter(division=division)
    return render(request, "gdanalyst/division.html", {
        "world": worldname,
        "division": division,
        "schools": school_list
    })

def get_distance(teamloc, teams):
    temp = {}
    #'tl' stands for team location
    tl = teamloc
    for team in teams:
        loc = School.objects.get(id=team.id).location
        dist = round(distance(tl.latitude, loc.latitude, tl.longitude, loc.longitude))
        temp[team.wis_id] = dist
    return temp

# No longer used
# def map(request):
#    return render(request, "gdanalyst/map.html")
'''
def player(request, worldname, division):
    playerid = request.GET['recruit']
    playerURL = f"https://www.whatifsports.com/gd/RecruitProfile/Ratings.aspx?rid={playerid}"
    headers = {'User-Agent': 'gdanalyst-get-player/1.1.5 python-requests/2.25.1', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
    playerpage = requests.get(playerURL, headers=headers)
    soup = BeautifulSoup(playerpage.content, 'lxml')
    name = soup.find(id="ctl00_ctl00_ctl00_Main_Main_name")
    position = soup.find(id="ctl00_ctl00_ctl00_Main_Main_position")
    hometown = soup.find(id="ctl00_ctl00_ctl00_Main_Main_homeTown")
    if hometown.text == "":
        return HttpResponse(f"Could not find recruit ID = " + escape(playerid))
    else:
        #print(name.text)
        #print(position.text)
        #print(hometown.text)
        hct = School.objects.exclude(coach="Sim AI").filter(world=worldname).filter(division=division)
        player_school_distance = get_distance_from(hometown.text, hct)
        if player_school_distance == 1:
            return HttpResponse(f"Could not find a location named {hometown.text}.")
        else:
            combined = {}
            for each in hct:
                combined[each.wis_id] = [each.school_short, each.coach, player_school_distance[0][each.wis_id], each.location.latitude, each.location.longitude]
            K = 2
            combined_sorted = sorted(combined.items(), key=lambda x: x[1][K])
            return render(request, "gdanalyst/player.html", {
                "player": name.text,
                "position": position.text,
                "hometown": hometown.text,
                "player_lat": player_school_distance[1],
                "player_lon": player_school_distance[2],
                "playerid": playerid,
                "world": worldname,
                "division": division,
                "hct": hct,
                "coachcount": len(hct),
                "combined": combined_sorted
            })
'''

def town(request, worldname, division):
    town_state = request.GET['town']
    hct = School.objects.exclude(coach="Sim AI").filter(world=worldname).filter(division=division)
    town_school_distance = get_distance_from(town_state, hct)
    if town_school_distance == 1:
        return HttpResponse(f"Could not find a location named " + escape(town_state))
    else:
        combined = {}
        for each in hct:
            combined[each.wis_id] = [each.school_short, each.coach, town_school_distance[0][each.wis_id], each.location.latitude, each.location.longitude]
        K = 2
        combined_sorted = sorted(combined.items(), key=lambda x: x[1][K])
        return render(request, "gdanalyst/town.html", {
            "hometown": town_state,
            "player_lat": town_school_distance[1],
            "player_lon": town_school_distance[2],
            "world": worldname,
            "division": division,
            "hct": hct,
            "coachcount": len(hct),
            "combined": combined_sorted
        })

def get_distance_from(player_or_loc, teams):
    temp = {}
    # Split into city and state
    playerloc_split = player_or_loc.split(',')
    # Town is first item in list
    town = playerloc_split[0]
    # State abbr is 2nd item in list and strip the leading space
    state_abbr = playerloc_split[1].strip()
    state_long = state_lookup(state_abbr)
    # Concatenate town + state + country
    playerloc =  f"{town}, {state_long}, USA"
    # Create URL to request lookup of location
    # Line below was old way that was not very robust and produced inconsistent results
    # find_location_url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(playerloc) + '?format=json'
    # Line below is new way that specifies city and state specifically in the search parameters
    find_location_url = f"https://nominatim.openstreetmap.org/search?city={town}&state={state_long}&country=USA&format=json"
    # https://nominatim.org/release-docs/develop/api/Search/
    headers = {'User-Agent': 'gdanalyst-get-distance/1.1.5 python-requests/2.25.1', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
    response = requests.get(find_location_url, headers=headers).json()
    if len(response) == 0:
        # This means response is emtpy and there was a problem
        return 1
    # Can potentially use this to confirm the returned location is from the intended state.
    # and return an error if they don't match.
    returned_display_name_info = [x.strip() for x in response[0]["display_name"].split(',')]
    if state_long not in returned_display_name_info:
        # If the intended state is different there was a problem
        return 1
    else:
        lat = float(response[0]["lat"])
        lon = float(response[0]["lon"])
        for team in teams:
            loc = School.objects.get(id=team.id).location
            dist = round(distance(lat, loc.latitude, lon, loc.longitude))
            temp[team.wis_id] = dist
        return temp, lat, lon

def state_lookup(state_abbr):
    states = {
        "AL":"Alabama",
        "AK":"Alaska",
        "AZ":"Arizona",
        "AR":"Arkansas",
        "CA":"California",
        "CO":"Colorado",
        "CT":"Connecticut",
        "DC":"District of Columbia",
        "DE":"Delaware",
        "FL":"Florida",
        "GA":"Georgia",
        "HI":"Hawaii",
        "ID":"Idaho",
        "IL":"Illinois",
        "IN":"Indiana",
        "IA":"Iowa",
        "KS":"Kansas",
        "KY":"Kentucky",
        "LA":"Louisiana",
        "ME":"Maine",
        "MD":"Maryland",
        "MA":"Massachusetts",
        "MI":"Michigan",
        "MN":"Minnesota",
        "MS":"Mississippi",
        "MO":"Missouri",
        "MT":"Montana",
        "NE":"Nebraska",
        "NV":"Nevada",
        "NH":"New Hampshire",
        "NJ":"New Jersey",
        "NM":"New Mexico",
        "NY":"New York",
        "NC":"North Carolina",
        "ND":"North Dakota",
        "OH":"Ohio",
        "OK":"Oklahoma",
        "OR":"Oregon",
        "PA":"Pennsylvania",
        "RI":"Rhode Island",
        "SC":"South Carolina",
        "SD":"South Dakota",
        "TN":"Tennessee",
        "TX":"Texas",
        "UT":"Utah",
        "VT":"Vermont",
        "VA":"Virginia",
        "WA":"Washington",
        "WV":"West Virginia",
        "WI":"Wisconsin",
        "WY":"Wyoming"
    }
    return states[state_abbr]

# Python 3 program to calculate Distance Between Two Points on Earth 
# From https://www.geeksforgeeks.org/program-distance-two-points-earth/#:~:text=For%20this%20divide%20the%20values,is%20the%20radius%20of%20Earth.
def distance(lat1, lat2, lon1, lon2): 
      
    # The math module contains a function named 
    # radians which converts from degrees to radians. 
    lon1 = radians(lon1) 
    lon2 = radians(lon2) 
    lat1 = radians(lat1) 
    lat2 = radians(lat2) 
       
    # Haversine formula  
    dlon = lon2 - lon1  
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  
    c = 2 * asin(sqrt(a))  
     
    # Radius of earth in kilometers. Use 3956 for miles. Use 6371 for KM
    r = 3956
       
    # calculate the result 
    return(c * r)      
# driver code  
# lat1 = 53.32055555555556
# lat2 = 53.31861111111111
# lon1 = -1.7297222222222221
# lon2 =  -1.6997222222222223
# print(distance(lat1, lat2, lon1, lon2), "K.M") 

def gameid(request):
    return render(request, "gdanalyst/gameid.html")

def recruitingCostCalc(request):
    return render(request, "gdanalyst/recruitingcostcalc.html")

def pbp(request):
    gid = request.GET['gameid']
    # Use with delay to use rqworker queue (production)
    gid_result = get_pbp.delay([gid])
    # Use without delay to bypass rqworker queue - used for debugging
    # gid_result = get_pbp([gid])
    if gid_result == 1:
        return 1
    else:
        base_url = reverse("loading_game_results")
        query_string = urlencode({'jobid': gid_result.id})
        url = "{}?{}".format(base_url, query_string)
        return redirect(url)

def teamschedule(request, wisid):
    wid = School.objects.get(wis_id=wisid)
    coach = wid.coach
    schedule_table = get_schedule_table(wisid)
    return render(request, "gdanalyst/schedule.html", {
        "wid": wid,
        "coach": coach,
        "schedule": schedule_table
    })


def get_all_results(request, wisid):
    gids = request.GET.getlist('gameids')
    schedule_table = get_schedule_table(wisid)
    results_job = ""
    if "all" in request.path:
        tmp = []
        for each in schedule_table:
            if each[6] != "#":
                tmp.append(each[6]) 
        if (all(i in tmp for i in gids)):
            print("The gameids that were passed are valid.")
        else:
            print("The gameids that were passed have produced an error.")
        # Use with delay to use rqworker queue (production)
        results_job =  get_pbp.delay(gids)
        # Use without delay to bypass rqworker queue - used for debugging
        # results_job =  get_pbp(tmp)
    elif "humans" in request.path:
        tmp = []
        for each in schedule_table:
            if each[4] != "Sim AI" and each[6] != "#":
                tmp.append(each[6]) 
        # Use with delay to use rqworker queue (production)
        results_job =  get_pbp.delay(tmp)
        # Use without delay to bypass rqworker queue - used for debugging
        # results_job =  get_pbp(tmp)
    base_url = reverse("loading_game_results")
    query_string = urlencode({'jobid': results_job.id})
    url = "{}?{}".format(base_url, query_string)
    return redirect(url)


def loading_game_results(request):
    job_id = request.GET.get('jobid')
    return render(request, "gdanalyst/gameresultsloading.html", {
        "job_id": job_id
    })


def jobstatus(request, jobid):
    # This is using native redis-cli
    # conn = get_redis_connection("default")
    conn = django_rq.get_connection('default')
    job = Job.fetch(jobid, connection=conn)
    return HttpResponse(job.get_status())


def display_game_results(request, jobid):
    conn = django_rq.get_connection('default')
    try:
        job = Job.fetch(jobid, connection=conn)
        print(f"job ID {jobid} size of result = {total_size(job.result)}")
    except Exception as e:
        return HttpResponse(f"Job does not exist. <br><br>Game Results are cached for 10 minutes. \
                            Either the game results have expired or there is a \
                            problem with the requested job.")
    if job.result == 1:
        # This implies error with gameid
        return HttpResponse(f"Error: Invalid GameID = " + escape(job.args[0]))
    else:
        return render(request, "gdanalyst/gameresult.html", {
            "result": job.result
    })

def get_schedule_table(wisid):
    team_schedule_URL = f"https://www.whatifsports.com/gd/TeamProfile/Schedule.aspx?tid={wisid}"
    headers = {'User-Agent': 'gdanalyst-get-schedule/1.1.5 python-requests/2.25.1', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
    team_schedule_page = requests.get(team_schedule_URL, headers=headers)
    soup = BeautifulSoup(team_schedule_page.content, 'lxml')
    schedule_headers = soup.find_all(class_="ContentBoxWrapper")
    gameresults_table = []
    for h in schedule_headers:
        header = h.find("h3")
        schedule_tables = h.find(class_="standard")
        tr_all = schedule_tables.find_all("tr")
        for tr in tr_all:
            temp_row = []
            td_all = tr.find_all("td")
            if len(td_all) != 0:
                # Exhibtion or Non-Conf or Conf or . . . 
                temp_row.append(header.text)

                # Date
                date = td_all[0].find(class_="ScoreboardLink").text
                temp_row.append(date)
                
                # Opponent text
                opp = td_all[1].find(class_="teamProfileLink")
                opponent = opp.text
                temp_row.append(opponent)
                
                # Opponent wis_id used to link to opponent
                opponent_href = opp['href']
                opponent_href_re = re.search(r'(\d{5})', opponent_href)
                opponent_id = opponent_href_re.group(1)
                temp_row.append(opponent_id)
                
                # Coach
                c = td_all[5].find(class_="coachProfileLink")
                temp_row.append(c.text)
                
                # Result text
                res = td_all[8].find(class_="boxscoreLink")
                result = res.text
                temp_row.append(result)
                
                # Result ID used to provide link to analyze box score
                if result != "":
                    result_href = res['href']
                    result_href_re = re.search(r'OpenBoxscore\((\d{7,8})', result_href)
                    if result_href_re is not None:
                        result_id = result_href_re.group(1)
                    else:
                        result_id = "#"
                else:
                    result_id = "#"
                temp_row.append(result_id)

                # Outcome
                outcome = td_all[9].text
                if outcome == "W" or outcome == "L":
                    temp_row.append(outcome)
                else:
                    temp_row.append("")

                gameresults_table.append(temp_row)
    return gameresults_table

def teamroster(wisid):
    QB = 0
    RB = 0
    WR = 0
    TE = 0
    OL = 0
    DL = 0
    LB = 0
    DB = 0
    K = 0
    P = 0

    team_roster_URL = f"https://www.whatifsports.com/gd/TeamProfile/Roster.aspx?tid={wisid}"
    headers = {'User-Agent': 'gdanalyst-get-roster/1.1.5 python-requests/2.25.1', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
    team_roster_page = requests.get(team_roster_URL, headers=headers)
    soup = BeautifulSoup(team_roster_page.content, 'lxml')

    # grabs the roster table
    roster_table = soup.find(id="tblRosterList")
    roster_table_body = roster_table.find("tbody")
    # need to find all rows first
    roster_rows = roster_table_body.find_all("tr")
    # then within each row, grab the text of the 3rd <td> element in the row (position)
    # then count each position
    for row in roster_rows:
        tmp = row.find_all("td")
        pos = tmp[2].text
        if pos == "QB":
            QB += 1
        if pos == "RB":
            RB += 1
        if pos == "WR":
            WR += 1
        if pos == "TE":
            TE += 1
        if pos == "OL":
            OL += 1
        if pos == "DL":
            DL += 1
        if pos == "LB":
            LB += 1
        if pos == "DB":
            DB += 1
        if pos == "K":
            K += 1
        if pos == "P":
            P += 1
    
    scholarships = 50 - (QB + RB + WR + TE + OL + DL + LB + DB + K + P)
    roster = {
        'Scholarships': scholarships,
        'QB': QB,
        'RB': RB,
        'WR': WR,
        'TE': TE,
        'OL': OL,
        'DL': DL,
        'LB': LB,
        'DB': DB,
        'K': K,
        'P': P 
        }
    return roster
    

def coach(request, coachid):
    teams = School.objects.filter(coach=coachid)
    return render(request, "gdanalyst/coach.html", {
        "teams": teams,
        "coach": coachid
    })

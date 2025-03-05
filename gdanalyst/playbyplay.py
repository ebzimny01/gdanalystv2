import requests
import time
import lxml
import re
import datetime
from bs4 import BeautifulSoup
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import django_rq
from django_rq import job
from nltk import tokenize
import os
import sys
import nltk

# Initialize NLTK data paths at the top of the file
def ensure_nltk_data():
    """Ensure NLTK data is available, particularly punkt_tab for tokenization."""
    nltk_data_dir = os.environ.get('NLTK_DATA', os.path.join(os.getcwd(), 'nltk_data'))
    
    # Add the NLTK data directory to the search path
    if nltk_data_dir not in nltk.data.path:
        nltk.data.path.insert(0, nltk_data_dir)
    
    # Check for punkt_tab specifically
    try:
        nltk.data.find('tokenizers/punkt_tab/english/')
    except LookupError:
        # Download punkt which contains punkt_tab
        nltk.download('punkt', download_dir=nltk_data_dir)
        
        # Create punkt_tab directory structure
        punkt_tab_dir = os.path.join(nltk_data_dir, 'tokenizers', 'punkt_tab')
        os.makedirs(os.path.join(punkt_tab_dir, 'english'), exist_ok=True)
        
        # Copy files from punkt to punkt_tab
        punkt_dir = os.path.join(nltk_data_dir, 'tokenizers', 'punkt')
        if os.path.exists(punkt_dir):
            for lang_dir in os.listdir(punkt_dir):
                lang_path = os.path.join(punkt_dir, lang_dir)
                if os.path.isdir(lang_path):
                    target_dir = os.path.join(punkt_tab_dir, lang_dir)
                    os.makedirs(target_dir, exist_ok=True)
                    for file in os.listdir(lang_path):
                        src_file = os.path.join(lang_path, file)
                        dst_file = os.path.join(target_dir, file)
                        if os.path.isfile(src_file) and not os.path.exists(dst_file):
                            with open(src_file, 'rb') as f_in:
                                with open(dst_file, 'wb') as f_out:
                                    f_out.write(f_in.read())

# Call this function when module is imported
ensure_nltk_data()

from .models import School
from .utils import total_size

@job
def get_pbp(gid_list):
    # Establish a sesssion connection to reuse in attempt to improve speed
    requests_session = requests.Session()
    
    # table to collect details for all GIDs in list
    all_table_data = []
    start = time.perf_counter()
    headers = {'User-Agent': 'gdanalyst-get-playbyplay/1.1.5 python-requests/2.25.1', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
    for gid in gid_list:
        game_baseURL = "https://www.whatifsports.com/gd/GameResults/BoxScore.aspx?gid="
        gamepage = requests_session.get(game_baseURL + str(gid), headers=headers)
        print(f"gamepage.content size = {total_size(gamepage.content)}")
        gamepage_soup = BeautifulSoup(gamepage.content, "lxml")
        team_away_tag = gamepage_soup.find(id="ctl00_ctl00_Main_Main_lnkAwayTeam")
        # If an invalid Game ID is entered, this next line will fail with KeyError exception
        try:
            team_away_href = team_away_tag.attrs['href']
        except KeyError:
            return 1
        team_away_href_re = re.search(r'(\d{5})', team_away_href)
        team_away_id = team_away_href_re.group(1)
        team_away_mod = School.objects.get(wis_id=team_away_id)
        team_away = team_away_mod.school_long
        team_away_short = team_away_mod.school_short
        team_home_tag = gamepage_soup.find(id="ctl00_ctl00_Main_Main_lnkHomeTeam")
        team_home_href = team_home_tag.attrs['href']
        team_home_href_re = re.search(r'(\d{5})', team_home_href)
        team_home_id = team_home_href_re.group(1)
        team_home_mod = School.objects.get(wis_id=team_home_id)
        team_home = team_home_mod.school_long
        team_home_short = team_home_mod.school_short
        
        # variable to keep track of which team is on offense
        offense = ""
        print(f"Away Team = {team_away}")
        print(f"Home Team = {team_home}")

        pbp_baseURL = "https://www.whatifsports.com/gd/GameResults/PlayByPlay.aspx?gid="
        pbp_q_suffix = ['&quarter=1&view=1', '&quarter=2&view=1', '&quarter=3&view=1', '&quarter=4&view=1']
        
        # table to collect details for single GID
        table_data = []

        # variable to keep track of which quarter is being evaluated
        quarter = 1

        for q in pbp_q_suffix:
            pbpURL = pbp_baseURL + str(gid) + q
            print(pbpURL)
            pbprawpage = requests_session.get(pbpURL)
            print(f"pbprawpage.content size = {total_size(pbprawpage.content)}")
            soup = BeautifulSoup(pbprawpage.content, 'lxml')
            pbp_table = soup.find(id="ctl00_ctl00_Main_Main_PBPTable")
            pbp_table_rows = pbp_table.find_all("tr")
            #print(pbp_table_rows)

            for tr in pbp_table_rows:
                t_row = []
                # Logic to find which team is on offense while iterating through rows
                tmp = ""
                if tr.find('h3'):
                    tmp = tr.find('h3').text
                if tmp == team_away:
                    offense = team_away_short
                    # iteration of this row should end and not append to table_data
                elif tmp == team_home:
                    offense = team_home_short
                else:
                    game = team_away_short + " @ " + team_home_short
                    t_row.append(game)                                          # column 0
                    t_row.append(offense)                                       # column 1
                    t_row.append(quarter)                                       # column 2
                    for td in tr.find_all("td"):
                        # first 'td' appended should be 'clock'                 # column 3
                        if td['class'][0] == "pbpClock":
                            clock_str = td.text
                            try:
                                clock_obj = datetime.datetime.strptime(clock_str, '%M:%S')
                            except:
                                clock_obj = datetime.datetime.strptime("0:00", '%M:%S')
                            t_row.append(clock_obj.strftime('%M:%S'))
                        elif td['class'][0] == "pbpBallOn" and td.text[0] != "\xa0":
                            # second 'td' appended should be 'ball on'          # column 4 (field position)
                            if "Own" in td.text:
                                t_row.append(int(td.text.replace('Own ', '')))
                            else:
                                t_row.append(100 - int(td.text))
                        elif td['class'][0] == "pbpDownDistance" and td.text[0] != "\xa0":
                            t_row.append(int(td.text[0]))                       # column 5 (down)
                            x = len(td.text)
                            t_row.append(int(td.text[(x - 2):x]))               # column 6 (distance)
                        
                        # continue parsing
                        # at this point the next item to append should be the play by play details which require special parsing
                        # i'm thinking of passing this off to separate function to parse
                        elif td['class'][0] == "pbpPlay" and td.find(class_='playHeader') != None:
                            parsed = parse_pbp(td)
                            for p in parsed:
                                t_row.append(p)
                        else:
                            t_row.append(td.text) # Home Score and Away get added here which adds two more columns (30 and 31)
                    #print(t_row)
                    #append entire row of data to data_table
                    if len(t_row) == 32:
                        # t_row[30] is the home team's score
                        # t_row[31] is the away team's score
                        score_margin = {
                            team_home_short: int(t_row[30]) - int(t_row[31]),
                            team_away_short: int(t_row[31]) - int(t_row[30])
                        }
                        print(score_margin)
                        print(offense)
                        t_row.append(score_margin[offense])
                        table_data.append(t_row)
            quarter += 1
        all_table_data += table_data
    duration = time.perf_counter() - start
    print(f"It took {duration:4.2f} seconds to parse play by play results for {len(gid_list)} games.")
    print(f"all_table_data size = {total_size(all_table_data)}")
    return all_table_data

def parse_pbp(p):
    result = []
    # gets text that includes offensive and defensive formations
    off_def_text = p.find(class_='playHeader').text
    r = re.search('\xa0\xa0OFF: (.+?)\xa0', off_def_text)
    
    
    off_players = {}
    def_players = {}

    # offensive formation
    if r.group(1) == "I-Formation":
        offense = "IForm"
        off_players = {
            'QB': '',
            'OL1': '',
            'OL2': '',
            'OL3': '',
            'OL4': '',
            'OL5': '',
            'TE': '',
            'RB1': '',
            'RB2': '',
            'WR1': '',
            'WR2': ''
        }
    elif r.group(1) == "Pro-Set":
        offense = "Pro"
        off_players = {
            'QB': '',
            'OL1': '',
            'OL2': '',
            'OL3': '',
            'OL4': '',
            'OL5': '',
            'TE': '',
            'RB1': '',
            'RB2': '',
            'WR1': '',
            'WR2': ''
        }
    elif r.group(1) == "Notre Dame Box":
        offense = "NDBox"
        off_players = {
            'QB': '',
            'OL1': '',
            'OL2': '',
            'OL3': '',
            'OL4': '',
            'OL5': '',
            'TE1': '',
            'TE2': '',
            'RB1': '',
            'RB2': '',
            'WR': ''
        }
    elif r.group(1) == "Wishbone":
        offense = "WB"
        off_players = {
            'QB': '',
            'OL1': '',
            'OL2': '',
            'OL3': '',
            'OL4': '',
            'OL5': '',
            'TE': '',
            'RB1': '',
            'RB2': '',
            'RB3': '',
            'WR': ''
        }
    elif r.group(1) == "Shotgun":
        offense = "Shot"
        off_players = {
            'QB': '',
            'OL1': '',
            'OL2': '',
            'OL3': '',
            'OL4': '',
            'OL5': '',
            'TE': '',
            'WR1': '',
            'WR2': '',
            'WR3': '',
            'WR4': ''
        }
    else:
        # this should be Trips
        offense = r.group(1)
        off_players = {
            'QB': '',
            'OL1': '',
            'OL2': '',
            'OL3': '',
            'OL4': '',
            'OL5': '',
            'TE': '',
            'RB': '',
            'WR1': '',
            'WR2': '',
            'WR3': ''
        }
    # find offensive player names and positions included in the play
    off_player_raw_text = p.find(id="offense").text
    for pos, name in off_players.items():
        tmp = re.search(f'{pos} ([\D]+) ([\D]+)', off_player_raw_text)
        if tmp is not None:
            off_players[pos] = tmp.group(1) + " " + tmp.group(2)
        else:
            print(f"ERROR parsing off_player_raw_text for:\n{p}\n")
            off_players[pos] = "ERROR ERROR"

    # defensive formation
    r = re.search('\xa0DEF: (.*)', off_def_text)
    defense = r.group(1)

    if defense == "3-4":
        def_players = {
            'DL1': '',
            'DL2': '',
            'DL3': '',
            'LB1': '',
            'LB2': '',
            'LB3': '',
            'LB4': '',
            'CB1': '',
            'CB2': '',
            'SS': '',
            'FS': ''
        }
    elif defense == "4-3":
        def_players = {
            'DL1': '',
            'DL2': '',
            'DL3': '',
            'DL4': '',
            'LB1': '',
            'LB2': '',
            'LB3': '',
            'CB1': '',
            'CB2': '',
            'SS': '',
            'FS': ''
        }
    elif defense == "4-4":
        def_players = {
            'DL1': '',
            'DL2': '',
            'DL3': '',
            'DL4': '',
            'LB1': '',
            'LB2': '',
            'LB3': '',
            'LB4': '',
            'CB1': '',
            'CB2': '',
            'FS': ''
        }
    elif defense == "5-2":
        def_players = {
            'DL1': '',
            'DL2': '',
            'DL3': '',
            'DL4': '',
            'DL5': '',
            'LB1': '',
            'LB2': '',
            'CB1': '',
            'CB2': '',
            'SS': '',
            'FS': ''
        }
    elif defense == "Nickel":
        def_players = {
            'DL1': '',
            'DL2': '',
            'DL3': '',
            'DL4': '',
            'LB1': '',
            'LB2': '',
            'CB1': '',
            'CB2': '',
            'CB3': '',
            'SS': '',
            'FS': ''
        }
    else:
        # this should mean defense is Dime
        def_players = {
            'DL1': '',
            'DL2': '',
            'DL3': '',
            'LB1': '',
            'LB2': '',
            'CB1': '',
            'CB2': '',
            'CB3': '',
            'CB4': '',
            'SS': '',
            'FS': ''
        }

    # find defensive player names and positions included in the play
    def_player_raw_text = p.find(id="defense").text
    for pos, name in def_players.items():
        tmp = re.search(f'{pos} ([\D]+) ([\D]+)', def_player_raw_text)
        if tmp is not None:
            def_players[pos] = tmp.group(1) + " " + tmp.group(2)
        else:
            print(f"ERROR parsing def_player_raw_text for:\n{p}\n")
            def_players[pos] = "ERROR ERROR"

    # gets play by play text
    t = p.find(class_='pbpDescription').text
    # splits out text into list of sentences
    try:
        t_sentences = tokenize.sent_tokenize(t)
    except LookupError:
        # If tokenization fails, ensure data is available and try again
        ensure_nltk_data()
        t_sentences = tokenize.sent_tokenize(t)
    t_sentences_length = len(t_sentences)

    # Column variables
    dt = ""                     # defensive type
    blitz = ""                  # if def blitzes this stores position that is blitzing
    ot = ""                     # offensive type
    rd = ""                     # run play direction
    pressure = ""               # defensive pressure on QB
    pd = ""                     # pass play depth
    pass_result = ""            # result of pass play
    pass_detail = ""            # more pass play details
    turnover = ""               # turnover?
    sack = ""                   # was QB sacked
    opm = ""                    # offensive play maker
    dpm = ""                    # defensive play maker
    cvrg = ""                   # defensive player in coverage
    cvr = ""                    # how well is the offensive player covered
    penalty = ""                # Was a penalty committed on the play
    td = ""                     # Was there a Touchdown scored on the play
    yg = 0                      # Yards gained on play
    ypen = ""                   # Penalty yards on play
    progression = ""            # QB progression for pass plays (should be num 1 to 5)
    progression_details = ""    # Details of progression

    # If sentence count = 1 then result of play is either a presnap PENALTY, spike the ball, or takes a knee
    if t_sentences_length == 1:
        only_sent_text = t_sentences[0]
        
        """
        Known pre-snap penalty names:
            Defensive Offsides	        (pre-snap)
            Delay of Game	            (pre-snap)
            Encroachment	            (pre-snap)
            False Start	                (pre-snap)
            Illegal Motion	            (pre-snap)
            IllegalFormation	        (pre-snap)
        """
        if "PENALTY" in only_sent_text:
            # g1 = PENALTY, g2 = player name, g3 = type of penalty, g4 = yards
            # penalty_info = re.search(r"^(\s?PENALTY).*\(([a-zA-z' ]*)\), (\w*\s?\w*\s?\w*), (\-?\d{1,2})", only_sent_text)
            # This one works when Penalty pbp does not include a player name in parantheses
            # g1 = type of penalty, g2 = yards
            penalty2_info = re.search(r"^\s?PENALTY on .*, (\w*\s?\w*\s?\w*), (\-?\d{1,2})", only_sent_text)
            try:
                penalty = penalty2_info.group(1)
            except:
                penalty = "ERR"
                print(f"Error(8) grabbing penalty info from pbp text:\n{only_sent_text}")
            ypen = penalty2_info.group(2)
            yg = ""
            ot = ""
        elif "spikes the ball" in only_sent_text:
            ot = "Ps"
            pass_result = "I"
            pass_detail = "Spike"
            opm_find = re.search(r"([a-zA-z'\- ]*) spikes the ball", only_sent_text)
            opm = opm_find.group(1)
            opm = find_off(opm, off_players)
            yg = 0
        elif "takes a knee" in only_sent_text:
            ot = "Rn"
            rd = "Knee"
            yg = -1
            opm_find = re.search(r"([a-zA-z'\- ]*) takes a knee", only_sent_text)
            opm = opm_find.group(1)
            opm = find_off(opm, off_players)
    else:
        dt_dict = {
            # first sentence is always focused on defensive play type if sentence count > 1
            "Defense lines up for a run.": "Rn",
            "Defense lines up for a pass with a cover Short.": "PsS",
            "Defense lines up for a pass with a cover Medium.": "PsM",
            "Defense lines up for a pass with a cover Long.": "PsL"
        }
        
        # sets defensive tendancy run or pass short, medium, long
        if t_sentences[0] in dt_dict:
            dt = dt_dict[t_sentences[0]]
        
        
        # if defense blitzes this will be second sentence
        if "Blitz" in t_sentences[1]:
            # this grabs the player's name who is blitzing
            blitz_by = re.search(r"Blitz by ([\w'-]+)\.", t_sentences[1])
            if blitz_by is not None:
                blitz = blitz_by.group(1)
                for pos, name in def_players.items():
                    if name.split()[1] == blitz:
                        blitz = pos
            else:
                blitz = "ERR"
                print(f"Error(7) using regular expression to find blitzing player in:\n{t}")

        # run or pass?
        if "takes the handoff and rushes" in t \
            or "takes the snap and rushes" in t \
            or "starts to scramble" in t \
            or "takes a knee" in t:
                # rushing play
                ot = "Rn"
                if "rushes wide." in t:
                    rd = "Out"
                if "rushes inside." in t:
                    rd = "In"
                if "scramble" in t:
                    rd = "Scr"
                if "takes a knee" in t:
                    rd = "Knee"
                # Fumbles appear to only happen on running plays
                if "fumbles the ball" in t and not re.search(r" fumbles the ball but it is recovered by .* to maintain possession", t):
                    turnover = "Fum"
                    dpm_find = re.search(r"([\w'-]+) makes the pick up", t)
                    dpm_find2 = re.search(r"It's recovered by ([\w'-]+)", t)
                    if dpm_find is not None:
                        dpm = dpm_find.group(1)
                        dpm = find_def(dpm, def_players)
                    elif dpm_find2 is not None:
                        dpm = dpm_find2.group(1)
                        dpm = find_def(dpm, def_players)
                    else:
                        dpm = "ERR"

        if "drops back to pass." in t or "lines up in shotgun and takes the snap" in t:
            # passing play
            ot = "Ps"
            

            # determines defensive line pressure on pass plays
            if "The offensive line is providing great time for" in t:
                pressure = -2
            if "The offensive line gets the first step" in t:
                pressure = -1
            if "The defensive line gets a good first step" in t:
                pressure = 1
            if "they are starting to break through." in t \
                or "The defensive line has broken through" in t \
                or "The defensive line has somehow broken through" in t:
                    pressure = 2
            if "The defensive line has somehow broken through to get great pressure on" in t:
                pressure = 3
        

            # for pass plays determines attempted pass depth
            if re.search(r"throws to .* behind the line of scrimmage \(very short\).", t):
                pd = "VS"
            if re.search(r"throws to .* \(Short\)", t):
                pd = "S"
            if re.search(r"throws to .* \(Medium\)", t):
                pd = "M"
            if re.search(r"throws to .* \(Long\)", t):
                pd = "L"
            if re.search(r"throws to .* \(Deep\)", t):
                pd = "D"
            
            pass_depth_lookup = {
                "Very Short": "VS",
                "Short": "S",
                "Medium": "M",
                "Long": "L",
                "Deep": "D",
                "Very Deep": "VD"
            }

            # Determine QB progression
            progression = 0
            for i in t_sentences:
                if "throws to " in i \
                    or "pulls in the catch in the end zone" in i \
                    or "reaches up to pull in the catch in the end zone" in i \
                    or "makes the catch in the end zone" in i:
                        progression += 1
                        break
                if " is well covered at the " in i:
                    # g1 = OP, g2 = DP, g3 = PD
                    progression_find = re.search(r"([\w'-]+) \(([\w'-]+,?[\w'-]*)\) is well covered at the .* \(([\w]+)\)\.", i)
                    o = progression_find.group(1)
                    o = find_off(o, off_players)
                    d = progression_find.group(2)
                    d = find_def(d, def_players)
                    pass_depth = pass_depth_lookup[progression_find.group(3)]
                    progression += 1
                    progression_details += str(progression) + f": {o},{d},WC,{pass_depth}. "
                if " is covered at the " in i:
                    # g1 = OP, g2 = DP, g3 = PD
                    progression_find = re.search(r"([\w'-]+) \(([\w'-]+,?[\w'-]*)\) is covered at the .* \(([\w]+)\)\.", i)
                    o = progression_find.group(1)
                    o = find_off(o, off_players)
                    d = progression_find.group(2)
                    d = find_def(d, def_players)
                    pass_depth = pass_depth_lookup[progression_find.group(3)]
                    progression += 1
                    progression_details += str(progression) + f": {o},{d},C,{pass_depth}. "
                if " can't get the pass off to " in i:
                    # g1 = OP, g2 = DP, g3 = PD
                    progression_find = re.search(r"can't get the pass off to ([\w'-]+) \(([\w'-]+,?[\w'-]*)\) at the .* \(([\w]+)\)\.", i)
                    o = progression_find.group(1)
                    o = find_off(o, off_players)
                    d = progression_find.group(2)
                    d = find_def(d, def_players)
                    pass_depth = pass_depth_lookup[progression_find.group(3)]
                    progression += 1
                    progression_details += str(progression) + f": {o},{d},_,{pass_depth}. "
                if " doesn't see the wide open " in i:
                    # g1 = OP, g2 = PD
                    progression_find = re.search(r"doesn't see the wide open ([\w'-]+) at the .* \(([\w]+)\)\.", i)
                    o = progression_find.group(1)
                    o = find_off(o, off_players)
                    pass_depth = pass_depth_lookup[progression_find.group(2)]
                    progression += 1
                    progression_details += str(progression) + f": {o},_,WO,{pass_depth}. "

            # to determine coverage and player in coverage for the thrown pass
            if "throws to a covered" in t:
                coverage_find = re.search(r" throws to a covered ([\w'-]+) \(([\w'-]+,?[\w'-]*)\)", t)
                if coverage_find is not None:
                    opm = coverage_find.group(1)
                    opm = find_off(opm, off_players)
                    cvrg = coverage_find.group(2)
                    cvrg = find_def(cvrg, def_players)
                    cvr = "C"
                    progression_details += str(progression) + f": {opm},{cvrg},{cvr},{pd}. "
                else:
                    opm = "ERROR"
                    cvrg = "ERROR"
                    cvr = "ERR"
                    print(f"ERROR(2) using regular expression to find OPM and CVRG in:\n{t}\n")
            elif "throws to a well-covered" in t:
                coverage_find = re.search(r" throws to a well-covered ([\w'-]+) \(([\w'-]+,?[\w'-]*)\)", t)
                if coverage_find is not None:
                    opm = coverage_find.group(1)
                    opm = find_off(opm, off_players)
                    cvrg = coverage_find.group(2)
                    cvrg = find_def(cvrg, def_players)
                    cvr = "WC"
                    progression_details += str(progression) + f": {opm},{cvrg},{cvr},{pd}. "
                else:
                    opm = "ERR"
                    cvrg = "ERR"
                    cvr = "ERR"
                    print(f"Error(3) using regular expression to find OPM and CVRG in:\n{t}")
            elif "throws to the wide open" in t:
                coverage_find = re.search(r" throws to the wide open ([\w'-]+) at the ", t)
                if coverage_find is not None:
                    opm = coverage_find.group(1)
                    opm = find_off(opm, off_players)
                    cvrg = ""
                    cvr = "WO"
                    progression_details += str(progression) + f": {opm},_,{cvr},{pd}. "
                else:
                    opm = "ERR"
                    cvrg = "ERR"
                    cvr = "ERR"
                    print(f"Error(4) using regular expression to find OPM and CVRG in:\n{t}")
            elif re.search(r"throws to .* behind the line of scrimmage", t):
                coverage_find = re.search(r"throws to ([\w'-]+?) behind the line of scrimmage \(very short\).", t)
                coverage_find2 = re.search(r"throws to ([\w'-]+?) \(([\w'-]+,?[\w'-]*)\) behind the line of scrimmage \(very short\).", t)
                if coverage_find is not None:
                    opm = coverage_find.group(1)
                    opm = find_off(opm, off_players)
                    progression_details += str(progression) + f": {opm},_,_,VS. "
                elif coverage_find2 is not None:
                    opm = coverage_find2.group(1)
                    opm = find_off(opm, off_players)
                    cvrg = coverage_find2.group(2)
                    cvrg = find_def(cvrg, def_players)
                    progression_details += str(progression) + f": {opm},{cvrg},_,VS. "
                else:
                    opm = "ERR"
                    cvrg = "ERR"
                    cvr = "ERR"
                    print(f"Error(5.1) using regular expression to find OPM and CVRG in:\n{t}")
            elif "catch in the end zone" in t:
                # g1 = OPM
                coverage_find1 = re.search(r"([\w'-]+?) pulls in the catch in the end zone", t)
                coverage_find2 = re.search(r"([\w'-]+?) makes the catch in the end zone", t)
                coverage_find3 = re.search(r"([\w'-]+?) reaches up to pull in the catch in the end zone", t)
                if coverage_find1 is not None:
                    opm = coverage_find1.group(1)
                    opm = find_off(opm, off_players)
                    progression_details += str(progression) + f": {opm},_,_,_. "
                elif coverage_find2 is not None:
                    opm = coverage_find2.group(1)
                    opm = find_off(opm, off_players)
                    progression_details += str(progression) + f": {opm},_,_,_. "
                elif coverage_find3 is not None:
                    opm = coverage_find3.group(1)
                    opm = find_off(opm, off_players)
                    progression_details += str(progression) + f": {opm},_,_,_. "
                else:
                    opm = "ERR"
                    cvrg = "ERR"
                    cvr = "ERR"
                    print(f"Error(5.2) using regular expression to find OPM and CVRG in:\n{t}")
            elif "throws to " in t:
                coverage_find = re.search(r" throws to ([\w'-]+?) \(([\w'-]+,?[\w'-]*)\)", t)
                if coverage_find is not None:
                    opm = coverage_find.group(1)
                    opm = find_off(opm, off_players)
                    cvrg = coverage_find.group(2)
                    cvrg = find_def(cvrg, def_players)
                    progression_details += str(progression) + f": {opm},{cvrg},_,{pd}. "
                else:
                    opm = "ERR"
                    cvrg = "ERR"
                    cvr = "ERR"
                    print(f"Error(5.2) using regular expression to find OPM and CVRG in:\n{t}")

            # capture info about incomplete pass
            if "Pass is overthrown." in t:
                pass_result = "I"
                pass_detail = "Ovr"
            if "Pass is thrown behind" in t:
                pass_result = "I"
                pass_detail = "Bhd"
            if "Pass is knocked down" in t:
                pass_result = "I"
                pass_detail = "KnD"
                dpm_find = re.search(r"Pass is knocked down by ([\w'-]+)\.", t)
                if dpm_find is not None:
                    dpm = dpm_find.group(1)
                    dpm = find_def(dpm, def_players)
                else:
                    dpm = "ERR"
            if "throws the ball away to avoid the sack" in t:
                pass_result = "I"
                pass_detail = "OoB"
                pressure = 3
            if "drops the pass." in t:
                pass_result = "I"
                pass_detail = "Drp"
            if "intercepts the ball" in t:
                pass_result = "I"
                pass_detail = "Int"
                turnover = "Int"
                dpm_find = re.search(r"([\w'-]+) intercepts the ball", t)
                if dpm_find is not None:
                    dpm = dpm_find.group(1)
                    dpm = find_def(dpm, def_players)
                else:
                    dpm = "ERR"
            # captures info about completed pass
            if "makes the catch." in t \
                or "makes the diving catch" in t \
                or "pulls in the catch" in t \
                or "catch in the end zone." in t \
                or "pull in the catch." in t \
                or "catches in a nice pass from" in t:
                    pass_result = "C"
            if "is sacked by " in t:
                sack = "Y"
                rd = "Sck"
                pressure = 4
                # regex g1 = last of sacked QB, g2 = last name of def player made sack, g3 = yards lost on sack
                sacked_find_opm_dpm = re.search(r"n?([\w'-]+) is sacked by ([\w'-]+) for a loss of (-?\d{1,2}) yards", t)
                if sacked_find_opm_dpm is not None:
                    opm = sacked_find_opm_dpm.group(1)
                    opm = find_off(opm, off_players)
                    dpm = sacked_find_opm_dpm.group(2)
                    dpm = find_def(dpm, def_players)
                else:
                    opm = "ERR"
                    dpm = "ERR"
                    print(f"Error(6) using regular expression to find OPM and dpm in:\n{t}")
        
        if "TOUCHDOWN" in t:
            td = "TD"

        if "SAFETY" in t:
            td = "SFTY"

        # Yards Gained
        # Removing this PENALTY if statement to attempt to rely on Penalty logic added further down below
        # if "PENALTY" not in t:
        for i in t_sentences:
            if "No gain on the play." in i:
                yg = 0
                dpm_find = re.search(r"is stopped by ([\w'-]+) at the line of scrimmage", i)
                if dpm_find is not None:
                    dpm = dpm_find.group(1)
                    dpm = find_def(dpm, def_players)
                else:
                    dpm = "ERR"
            elif "for a loss of " in i:
                # need to grab the negative yards
                yards_match = re.search(r"for a loss of -([\d]+) yard", i)
                yg = -int(yards_match.group(1))
                dpm_find = re.search(r"is .*? by ([\w'-]+) for a loss", i)
                if dpm_find is not None:
                    dpm = dpm_find.group(1)
                    dpm = find_def(dpm, def_players)
                else:
                    dpm = "ERR"
            elif "yards on the play." in i or "yard gain." in i or "yards gain." in i:
                # need to grab the positive yards
                yards_match = re.search(r'(^[\d-]+) yard', i)
                yg = int(yards_match.group(1))
        
        """
        Known post-snap penalty names:
            Defensive Holding	
            Defensive Pass Interference	
            DefensivePersonalFoul	
            Facemask
            Intentional Grounding	
            Offensive Holding	
            Offensive Pass Interference	
            OffensivePersonalFoul	
            Roughing The Passer	
        """

        if "PENALTY" in t and "yards, enforced at" in t and "yard Penalty added to the end of the play" not in t:
            # g1 = player name, g2 = type of penalty, g3 = yards
            penalty_info = re.search(r"\s?PENALTY.*?\(?([a-zA-z'\- ]*)?\)?,\s(\w*\s?\w*\s?\w*),?\s(\-?\d{1,2})", t)
            if penalty_info is not None:
                penalty = penalty_info.group(2)
                ypen = penalty_info.group(3)
            else:
                penalty = "ERR"
                ypen = "ERR"
                print(f"Error(20): regex could not find match for a penalty play.\npbptext = {t}")
            
            # Treating these penalties as if the play didn't happen.
            # Any offensive yards gained are removed and pass_result removed.
            # Leaving other variables untouched.
            if penalty == "Defensive Holding" or penalty == "Defensive Pass Interference" \
                or penalty == "Offensive Holding" or penalty == "Offensive Pass Interference" \
                or penalty == "OffensivePersonalFoul":
                    pass_result = ""
                    yg = ""
        elif "PENALTY" in t and "yard Penalty added to the end of the play" in t:
            # g1 = player name, g2 = type of penalty, g3 = yards
            penalty_info = re.search(r"\s?PENALTY.*\(([a-zA-z'\- ]*)\),\s(.*)\.\s(\d{1,2}) yard Penalty added to the end of the play\.", t)
            penalty = penalty_info.group(2)
            ypen = penalty_info.group(3)
            turnover = ""
            if yg < 0:
                yg = ""

        # OPM - offensive play maker
        for i in t_sentences:
            if (rd == "Out" or rd == "In") \
                and ("takes the handoff" in i or "takes the snap and rushes" in i):
                    opm_find = re.search(r"(^[\w'-]+ [\w'-]+) takes the [\w]+ and rushes", i)
                    if opm_find is not None:
                        opm = opm_find.group(1)
                        opm = find_off(opm, off_players)
                    else:
                        opm = "ERR"
            if rd == "Scr" and "starts to scramble" in i:
                opm_find = re.search(r"(^[\w'-]+) starts to scramble", i)
                if opm_find is not None:
                    opm = opm_find.group(1)
                    opm = find_off(opm, off_players)
                else:
                    opm = "ERR"
            if ot == "Ps" and pass_result == "C":
                for i in t_sentences:
                    if "catch" in i:
                        opm = i.split()[0]
                        opm = find_off(opm, off_players)

        # DPM - defensive play maker
        for i in t_sentences:
            if "is tackled by" in i:
                dpm_find = re.search(r" is tackled by ([\w'-]+) at the", i)
                if dpm_find is not None:
                    dpm = dpm_find.group(1)
                    dpm = find_def(dpm, def_players)
                else:
                    dpm = "ERR"
            if "gets a hand on" in i:
                dpm_find = re.search(r"^([\w'-]+) gets a hand on ", i)
                if dpm_find is not None:
                    dpm = dpm_find.group(1)
                    dpm = find_def(dpm, def_players)
                else:
                    dpm = "ERR"
            if "is brought down by" in i:
                dpm_find = re.search(r" is brought down by ([\w'-]+) ", i)
                if dpm_find is not None:
                    dpm = dpm_find.group(1)
                    dpm = find_def(dpm, def_players)
                else:
                    dpm = "ERR"

    # modifies play by play to print each sentence out on new line
    tmp_sent = ""
    for sent in t_sentences:
        tmp_sent = tmp_sent + sent + "\n"
    
    result.append(offense)              # index 7
    result.append(defense)              # index 8
    result.append(dt)                   # index 9
    result.append(blitz)                # index 10
    result.append(ot)                   # index 11
    result.append(rd)                   # index 12
    result.append(pressure)             # index 13
    result.append(pd)                   # index 14
    result.append(cvrg)                 # index 15
    result.append(cvr)                  # index 16
    result.append(pass_result)          # index 17
    result.append(pass_detail)          # index 18
    result.append(sack)                 # index 19
    result.append(penalty)              # index 20
    result.append(turnover)             # index 21
    result.append(td)                   # index 22
    result.append(yg)                   # index 23
    result.append(opm)                  # index 24
    result.append(dpm)                  # index 25
    result.append(tmp_sent)             # index 26
    result.append(ypen)                 # index 27
    result.append(progression)          # index 28
    result.append(progression_details)  # index 29

    return result

def find_off(o, off_dict):
    for pos, name in off_dict.items():
        if name == o or name.split()[1] == o:
            o = pos
    return o

def find_def(d, def_dict):
    if "," in d:
        # This means two defensive players were covering offensive player
        # Need to split up, match each position and return back
        tmp = d.split(",")
        for pos, name in def_dict.items():
            if name == tmp[0] or name.split()[1] == tmp[0]:
                d = pos
        for pos, name in def_dict.items():
            if name == tmp[1] or name.split()[1] == tmp[1]:
                d += "," + pos
    else:
        for pos, name in def_dict.items():
            if name == d or name.split()[1] == d:
                d = pos
    return d

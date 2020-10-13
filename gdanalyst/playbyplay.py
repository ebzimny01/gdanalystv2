import requests, urllib.parse, html5lib, lxml, re, datetime
from bs4 import BeautifulSoup
import nltk
from nltk import tokenize
nltk.download('punkt')
# import pandas as pd
from .models import School

def get_pbp(gid):
    game_baseURL = "https://www.whatifsports.com/gd/GameResults/BoxScore.aspx?gid="
    gamepage = requests.get(game_baseURL + str(gid))
    gamepage_soup = BeautifulSoup(gamepage.content, "html.parser")
    team_away_tag = gamepage_soup.find(id="ctl00_ctl00_Main_Main_lnkAwayTeam")
    team_away_href = team_away_tag.attrs['href']
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
    
    # variable to keep track of which quarter is being evaluated
    quarter = 1

    # table to collect details
    table_data = []

    for q in pbp_q_suffix:
        pbpURL = pbp_baseURL + str(gid) + q
        print(pbpURL)
        pbprawpage = requests.get(pbpURL)

        soup = BeautifulSoup(pbprawpage.content, 'html.parser')
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
                        # second 'td' appended should be 'ball on'  
                        clock_str = td.text
                        try:
                            clock_obj = datetime.datetime.strptime(clock_str, '%M:%S')
                        except:
                            clock_obj = datetime.datetime.strptime("0:00", '%M:%S')
                        t_row.append(clock_obj.strftime('%M:%S'))           # column 4
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
                        t_row.append(td.text)
                #print(t_row)
                #append entire row of data to data_table
                if len(t_row) == 29:
                    table_data.append(t_row)
        quarter += 1

    #for i in table_data:
    #    print(i)
    return table_data

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
    result.append(offense)  # index 0
    
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
    result.append(defense)  # index 1

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
    t_sentences = tokenize.sent_tokenize(t)
    
    dt_dict = {
        # first sentence is always focused on defensive play type
        "Defense lines up for a run.": "Run",
        "Defense lines up for a pass with a cover Short.": "PsS",
        "Defense lines up for a pass with a cover Medium.": "PsM",
        "Defense lines up for a pass with a cover Long.": "PsL"
    }
    
    # sets defensive tendancy run or pass short, medium, long
    dt = ""
    if t_sentences[0] in dt_dict:
        dt = dt_dict[t_sentences[0]]
    result.append(dt)       # index 2
    
    # if defense blitzes this will be second sentence
    blitz = ""
    if len(t_sentences) > 1:
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
    else:
        blitz = ""
    result.append(blitz)    # index 3

    # run or pass?
    ot = ""
    rd = ""
    if "takes the handoff and rushes" in t or "starts to scramble" in t:
        # rushing play
        ot = "Rn"
        if "rushes wide." in t:
            rd = "Out"
        if "rushes inside." in t:
            rd = "In"
        if "scramble" in t:
            rd = "Scr"

    pressure = ""
    pd = ""
    pass_result = ""
    pass_detail = ""
    turnover = ""
    sack = ""
    opm = ""
    dpm = ""
    cvrg = ""
    cvr = ""
    if "drops back to pass." in t:
        # passing play
        ot = "Ps"
        

        # determines defensive line pressure on pass plays
        if "The defensive line has broken through" in t:
            pressure = 2
        if "The defensive line has somehow broken through" in t:
            pressure = 2
        if "they are starting to break through." in t:
            pressure = 1
       

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
        
        # to determine coverage and player in coverage
        if "throws to a covered" in t:
            coverage_find = re.search(r" throws to a covered ([\w'-]+) \(([\w'-]+,?[\w'-]*)\)", t)
            if coverage_find is not None:
                opm = coverage_find.group(1)
                opm = find_off(opm, off_players)
                cvrg = coverage_find.group(2)
                cvrg = find_def(cvrg, def_players)
                cvr = "C"
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
            else:
                opm = "ERR"
                cvrg = "ERR"
                cvr = "ERR"
                print(f"Error(4) using regular expression to find OPM and CVRG in:\n{t}")
        elif "throws to " in t:
            coverage_find = re.search(r" throws to ([\w'-]+?) \(([\w'-]+,?[\w'-]*)\)", t)
            if coverage_find is not None:
                opm = coverage_find.group(1)
                opm = find_off(opm, off_players)
                cvrg = coverage_find.group(2)
                cvrg = find_def(cvrg, def_players)
            else:
                opm = "ERR"
                cvrg = "ERR"
                cvr = "ERR"
                print(f"Error(5) using regular expression to find OPM and CVRG in:\n{t}")

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
            pressure = 2
        if "drops the pass." in t:
            pass_result = "I"
            pass_detail = "Drp"
        if "INTERCEPTED by" in t:
            pass_result = "I"
            pass_detail = "Int"
            turnover = "Int"
        # captures info about completed pass
        if "makes the catch." in t or "makes the diving catch" in t or "pulls in the catch." in t or "pull in the catch." in t:
            pass_result = "C"
        # 
        if "is sacked by " in t:
            sack = "Y"
            sacked_find_opm_dpm = re.search(r". ([\w'-]+) is sacked by ([\w'-]+) for a loss", t)
            if sacked_find_opm_dpm is not None:
                opm = sacked_find_opm_dpm.group(1)
                opm = find_off(opm, off_players)
                dpm = sacked_find_opm_dpm.group(2)
                dpm = find_def(dpm, def_players)
            else:
                opm = "ERR"
                dpm = "ERR"

    result.append(ot)           # index 4
    result.append(rd)           # index 5
    result.append(pressure)     # index 6
    result.append(pd)           # index 7
    result.append(cvrg)         # index 8
    result.append(cvr)          # index 9
    result.append(pass_result)  # index 10
    result.append(pass_detail)  # index 11
    result.append(sack)         # index 12

    if "PENALTY" in t:
        penalty = "Y"
    else:
        penalty = ""
    result.append(penalty)      # index 13

    if "FUMBLE" in t:
        turnover = "Fum"
    else:
        turnover = ""
    result.append(turnover)     # index 14

    if "TOUCHDOWN" in t:
        td = "TD"
    else:
        td = ""
    result.append(td)           # index 15

    # Yards Gained
    yg = 0                      # index 16
    if "PENALTY" not in t:
        if t_sentences[-1] == "No gain on the play.":
            yg = 0
            dpm_find = re.search(r"is stopped by ([\w'-]+) at the line of scrimmage", t)
            if dpm_find is not None:
                dpm = dpm_find.group(1)
                dpm = find_def(dpm, def_players)
            else:
                dpm = "ERR"
        elif "for a loss of " in t_sentences[-1]:
            # need to grab the negative yards
            yards_match = re.search(r"for a loss of -([\d]+) yard", t_sentences[-1])
            yg = -int(yards_match.group(1))
            dpm_find = re.search(r"is .*? by ([\w'-]+) for a loss", t)
            if dpm_find is not None:
                dpm = dpm_find.group(1)
                dpm = find_def(dpm, def_players)
            else:
                dpm = "ERR"
        elif "yards on the play" in t_sentences[-1] or "yard gain" in t_sentences[-1] or "yards gain" in t_sentences[-1]:
            # need to grab the positive yards
            yards_match = re.search(r'(^[\d-]+) yard', t_sentences[-1])
            yg = int(yards_match.group(1))
        elif "TOUCHDOWN" in t_sentences[-1]:
            yards_match = re.search(r'(^[\d-]+) yard', t_sentences[-2])
            yg = int(yards_match.group(1))
    result.append(yg)           # index 17

    # OPM - offensive play maker
    for i in t_sentences:
        if (rd == "Out" or rd == "In") and "takes the handoff" in i:
            opm_find = re.search(r"(^[\w'-]+ [\w'-]+) takes the handoff", i)
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

    result.append(opm)          # index 18
    result.append(dpm)          # index 19

    # modifies play by play to print each sentence out on new line
    tmp_sent = ""
    for sent in t_sentences:
        tmp_sent = tmp_sent + sent + "\n"
    result.append(tmp_sent)            # index 20

    return result

def find_off(o, off_dict):
    for pos, name in off_dict.items():
        if name == o or name.split()[1] == o:
            o = pos
    return o

def find_def(d, def_dict):
    for pos, name in def_dict.items():
        if name == d or name.split()[1] == d:
            d = pos
    return d

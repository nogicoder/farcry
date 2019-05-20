#!/usr/bin/python3

# Emoji Icons
CHARACTER_BOAT = '🚤'
CHARACTER_AUTOMOBILE = '🚙'
CHARACTER_VICTIM = '😦'
CHARACTER_KILLER = '😛'
CHARACTER_SUICIDE = '☠'
CHARACTER_GUN = '🔫'
CHARACTER_GRENADE = '💣'
CHARACTER_ROCKET = '🚀'
CHARACTER_MACHETE = '🔪'

weapon_icon = {
    'Vehicle': CHARACTER_AUTOMOBILE,
    'Falcon': CHARACTER_GUN,
    'Shotgun': CHARACTER_GUN,
    'P90': CHARACTER_GUN,
    'MP5': CHARACTER_GUN,
    'MG': CHARACTER_GUN,
    'M4': CHARACTER_GUN,
    'AG36': CHARACTER_GUN,
    'OICW': CHARACTER_GUN,
    'SniperRifle': CHARACTER_GUN,
    'M249': CHARACTER_GUN,
    'VehicleMountedAutoMG': CHARACTER_GUN,
    'VehicleMountedMG': CHARACTER_GUN,
    'HandGrenade': CHARACTER_GRENADE,
    'AG36Grenade': CHARACTER_GRENADE,
    'OICWGrenade': CHARACTER_GRENADE,
    'StickyExplosive': CHARACTER_GRENADE,
    'Rocket': CHARACTER_ROCKET,
    'VehicleMountedRocketMG': CHARACTER_ROCKET,
    'VehicleRocket': CHARACTER_ROCKET,
    'Machete': CHARACTER_MACHETE,
    'Boat': CHARACTER_BOAT
}


def read_log_file(log_file_pathname):
    """
    Waypoint 1: Read Game Session Log File
    ---
    Check if file exists, read and return the content.
    If it don't exist, throw error and exit program
    ---
    @param {str} log_file_pathname: path of log file
    @return {str} log_data: content of log file
    """
    from os.path import isfile

    if isfile(log_file_pathname):
        data = open(log_file_pathname, "r")
        if data.mode == 'r':
            log_data = data.read()
            return log_data
    else:
        print("FileNotFoundError: No such file or directory: '" + log_file_pathname + "'")
        exit(0)


def parse_log_start_time(log_data):
    """
    Waypoint 2 + 3: Parse Far Cry Engine's Start Time + Time Zone
    ---
    Parse date and time information to determine later the timestamp of each frag.
    ---
    @param {str} log_data: content of log file
    @return {object} start_time:(datetime.datetime) represent the time the Far Cry engine started to log at.

    """

    from datetime import datetime
    from datetime import timedelta
    from datetime import timezone

    # get time zone
    index_timezone = log_data.find('g_timezone') + 11
    value_timezone = log_data[index_timezone: index_timezone+5].split('\n')[0][:-1]
    g_timezone = timezone(timedelta(hours=int(value_timezone)))

    # get local start time
    first_line = log_data.split('\n')[0][15:]
    format_form = "%A, %B %d, %Y %H:%M:%S" # Friday, November 09, 2018 12:22:07
    start_time_local = datetime.strptime(first_line, format_form)

    # add timezone into local start time
    start_time = start_time_local.replace(tzinfo=g_timezone)

    return start_time


def parse_match_mode_and_map(log_data):
    """
    Waypoint 4: Parse Match Session's Mode and Map

    Find more (mode, map) in 3,4,5,7,8,9, 10
    ---
    @param {str} log_data: content of log file
    @return {tuple} (mode, map).

    """
    from re import findall

    mode_and_map = findall(".* Loading level Levels\/(.*), mission (.*) -.*", log_data)

    return mode_and_map


def parse_frags(log_data):
    """
    Waypoint 5: Parse Frag History
    Waypoint 6: Include Time Zone To Frag Timestamps
    ---
    @param {str} log_data: content of log file
    @return {list(tuple)} frags: infomation of each frag(time*, killer*, victim, weapon)
    *: require
    non-*: optional
    """

    from re import findall
    from datetime import datetime
    from datetime import timedelta

    # (frag_time, killer_name)
    # (frag_time, killer_name, victim_name, weapon_code)
    # <(frag_time*)> <Lua> (killer_name*) killed (victim_name) itself/with ( weapon_code)

    patterm = "<(\d{2}:\d{2})> <.*> (.*) killed (.*)(itself| with)(.*)"
    rough_frags = findall(patterm, log_data)

    start_time = parse_log_start_time(log_data)
    start_hour = start_time.hour
    frags = []

    for frag in rough_frags:
        frag_time = start_time.replace(minute=int(frag[0][:2]), second=int(frag[0][3:]))
        if frag_time < start_time:
            frag_time = start_time.replace(hour=start_hour+1, minute=int(frag[0][:2]), second=int(frag[0][3:]))
        line = list(frag)
        line.pop(0) # del time
        line.pop(2) # del with/itself

        if line[1] == '': # clear when player is killed by itself
            line.pop()
            line.pop()

        if len(frag[-1]) > 0: # del space
            line[-1] = frag[-1][1:]
        line = [frag_time] + line # combine frag
        frags.append(tuple(line)) # add to big frags
    rough_frags.clear()
    return frags


def prettify_frags(frags):
    """
    Waypoint 7: Prettify Frag History
    KeyError 'MG' 1, 3, 4, 5, 7, 8, 9
    adding 'MG' in emoji table
    """
    prettified_frags = []
    for frag in frags:
        if len(frag) == 4: # (frag_time, killer_name, victim_name, weapon_code)
            line = '[' + frag[0].isoformat() + '] ' + CHARACTER_KILLER + '  ' + frag[1] + ' ' + weapon_icon[frag[3]] + '  ' + CHARACTER_VICTIM + '  ' + frag[2]
        else: # len = 2 (frag_time, killer_name)
            line = '[' + frag[0].isoformat() + '] ' + CHARACTER_VICTIM + '  ' + frag[1] + ' ' + CHARACTER_SUICIDE
        prettified_frags.append(line)

    return prettified_frags


def parse_game_session_start_and_end_times(log_data):
    """
    Waypoint 8: Determine Game Session's Start and End Times
    ---
    :param {str} log_data: content of log file
    :return {tuple(start, end)}:
    non statistics log01.tsxt
    more then one statistics log05.txt
    """
    # from re import findall
    # start = findall(r"<.*> Precaching level ... <(.*)> done", log_data)[0].split(':')
    # end = findall(r"<(.*)> == Statistics.*==", log_data)[0]
    # if end:
    #     end = end.split(':')
    # else:
    #     end = findall(r"<(.*)> ERROR: .3#SCRIPT ERROR File: =C, Function: _ERRORMESSAGE,", log_data)[0].split(':')
    # start_session = dictionary_data['start_time'].replace(minute=int(start[0]), second=int(start[1]))
    # end_session = dictionary_data['start_time'].replace(minute=int(end[0]), second=int(end[1]))
    # result = (start_session, end_session)
    # return result


def write_frag_csv_file(file_csv, frags):
    """
    Waypoint 9: Create Frag History CSV File
    ---
    @param {str} file_csv: name of new csv file
    @param {list(tuple)} frags: infomation of each frag(time*, killer*, victim, weapon)
    @return: create csv file
    """
    import csv

    with open(file_csv, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(frags)

    csvFile.close()



if __name__ == "__main__":
    import json

    log_data = read_log_file("../logs/log00.txt")
    print(len(log_data))
    wp2_3 = parse_log_start_time(log_data)
    # print(wp2_3)

    wp4 = parse_match_mode_and_map(log_data)
    # print(wp4, type(wp4))

    wp5_6 = parse_frags(log_data)
    # print(wp5_6)
    # my_json_string = json.dumps(wp5_6,indent=2)
    # print(my_json_string)

    wp7 = prettify_frags(wp5_6)
    # print('\n'.join(wp7))

    wp8 = parse_game_session_start_and_end_times(log_data)
    # not yet

    write_frag_csv_file('log04.csv', wp5_6) #wp9

    # Waypoint 10: Import CSV File into Google Sheets
    """
    link file
    https://docs.google.com/spreadsheets/d/1uULqLIZxmcfraa4Ulu-v2ysz1qH9Fv1BpsBrJ90V5II/edit#gid=749971819
    """

    # wp 11: Collect the List of Players
    """
    column 'F': =ARRAYFORMULA(SORT(UNIQUE(FILTER({B:B;C:C}; NOT(ISBLANK({B:B; C:C}))))))
    """

    # wp 12: Calculate Match Statistics
    """
    column 'G': =ARRAYFORMULA(COUNTIF(B:B;F1))
    column 'H': =ARRAYFORMULA(COUNTIF(C:C;F1))
    column 'I': =COUNTIFS(B:B; F1; C:C;"=")
    column 'J': =ROUND(G1/(G1+H1+I1)*100; 2)
    """

    # wp 13: Split Frag History and Match Statistics into 2 Sheets
    """
    column 'A' =ARRAYFORMULA(SORT(UNIQUE(FILTER({'{SHEET_NAME}'!B:B;'{SHEET_NAME}'!C:C}; NOT(ISBLANK({'{SHEET_NAME}'!B:B; '{SHEET_NAME}'!C:C}))))))
    column 'B' =ARRAYFORMULA(COUNTIF('{SHEET_NAME}'!B:B;A3))
    column 'C' =ARRAYFORMULA(COUNTIF('{SHEET_NAME}'!C:C;A3))
    column 'D' =COUNTIFS('{SHEET_NAME}'!B:B; A3; '{SHEET_NAME}'!C:C;"=")
    column 'E' =B3/(B3+C3+D3)

    """

    # wp 14: Calculate the Overall Statistics of a Match
    """
    'Kills' =SUM(B$3:B)
    'Deaths' =SUM(C$3:C)
    'Suicides' =SUM(D$3:D)
    """

    #

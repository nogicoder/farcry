# Emoji Icons - wp7
CHARACTER_BOAT = '🚤'
CHARACTER_AUTOMOBILE = '🚙'
CHARACTER_VICTIM = '😦'
CHARACTER_KILLER = '😛'
CHARACTER_SUICIDE = '☠'
CHARACTER_GUN = '🔫'
CHARACTER_GRENADE = '💣'
CHARACTER_ROCKET = '🚀'
CHARACTER_MACHETE = '🔪'

# wp7
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


    # get time zone - wp3 
    index_timezone = log_data.find('g_timezone') + 11
    value_timezone = log_data[index_timezone: index_timezone+5].split('\n')[0][:-1]
    g_timezone = timezone(timedelta(hours=int(value_timezone)))

    # get local start time - wp2
    first_line = log_data.split('\n')[0][15:]
    format_form = "%A, %B %d, %Y %H:%M:%S" # Friday, November 09, 2018 12:22:07
    start_time_local = datetime.strptime(first_line, format_form)

    # add timezone into local start time
    start_time = start_time_local.replace(tzinfo=g_timezone)

    return start_time


def parse_match_mode_and_map(log_data):
    """
    Waypoint 4: Parse Match Session's Mode and Map
    ---
    Scaning all line and return the FIRST LINE matches the pattern

    NOTE: Find more (mode, map) in 4, 5, 7, 8, 9, 10, 11
    ---
    @param {str} log_data: content of log file
    @return {tuple} (mode, map).

    """
    from re import findall

    # format: ... Loading level Levels/(map), mission (mode) ...
    pattern = ".* Loading level Levels\/(.*), mission (.*) -.*"
    mode_and_map = findall(pattern, log_data)

    return (mode_and_map[0][::-1])


def parse_frags(log_data):
    """
    Waypoint 5: Parse Frag History
    Waypoint 6: Include Time Zone To Frag Timestamps
    ---
    Find all lines that match with the format:
        + <{MM:SS}> <Lua> {killer_username} killed {victim_username} with {weapon_code}
        + <{MM:SS}> <Lua> {killer_username} killed itself
    ---
    @param {str} log_data: content of log file
    @return {list(tuple)} frags: infomation of each frag (time{object}*, killer{str}*, victim{str}, weapon{str})
    """

    from re import findall
    from datetime import datetime
    from datetime import timedelta

    # <{frag_time}*)> <Lua> {killer_name}* killed {victim_name} {itself/with} { weapon_code}
    pattern = "<(\d{2}:\d{2})> <Lua> (.*) killed (.*)(itself| with)(.*)"
    rough_frags = findall(pattern, log_data)

    # get the engine's Start Time - wp3
    start_time = parse_log_start_time(log_data)
    start_hour = start_time.hour

    frags = []

    for frag in rough_frags:
        # increase the hours by 1 manually.
        frag_time = start_time.replace(minute=int(frag[0][:2]), second=int(frag[0][3:]))
        if frag_time < start_time:
            frag_time = frag_time.replace(hour=start_hour+1)
        
        line = list(frag) # convert tuple to list 

        line.pop(3) # delete itself/with

        if len(frag[-1]) != 0: #  delete a space in 'with' case
            line[-1] = frag[-1][1:]
        else: # delete empty str in 'itself' case
            line.pop()
            line.pop()

        line = [frag_time] + line[1:] # combine frag
        # print(line)
        frags.append(tuple(line)) # add to big frags

    rough_frags.clear()
    return frags


def prettify_frags(frags):
    """
    Waypoint 7: Prettify Frag History
    ---
    Adding icon with the format:
        + [frag_time] 😛 killer_name weapon_icon 😦 victim_name
        + [frag_time] 😦 victim_name ☠
    ---
    @param {list(tuple)} frags: information of each frag
    @return {list(tuple)} prettified_frags: frag with emotion 

    """
    prettified_frags = []
    for frag in frags:
        if len(frag) == 4: # (frag_time, killer_name, victim_name, weapon_code)
            line = '[' + frag[0].isoformat() + '] ' + CHARACTER_KILLER + '  ' + frag[1] + ' ' + weapon_icon[frag[3]] + '  ' + CHARACTER_VICTIM + '  ' + frag[2]
        else: # len = 2 (frag_time, killer_name)
            line = '[' + frag[0].isoformat() + '] ' + CHARACTER_VICTIM + '  ' + frag[1] + ' ' + CHARACTER_SUICIDE
        prettified_frags.append(line)

    return prettified_frags


def parse_game_session_start_and_end_times(log_data, frags):
    """
    Waypoint 8: Determine Game Session's Start and End Times
    ---
    START: <start_time> Precaching level --- <{start_time} done
    END: 
        + <end_time> *. Statistics .* => run
        + <end_time> last frag => crash

    NOTE:
    non statistics log01.tsxt
    more then one statistics log05.txt
    ---
    @param {str} log_data: content of log file
    @return {tuple(start(object), end(object))}: start time and end time
    """

    from re import findall

    pattern_start = "<.*> Precaching level ... <(.*)> done"
    start_time = findall(pattern_start, log_data)[0].split(':')

    start_log = parse_log_start_time(log_data)
    start_session = start_log.replace(minute=int(start_time[0]), second=int(start_time[1]))

    pattern_end_run = "<(.*)>.*Statistics.*"
    end_time = findall(pattern_end_run, log_data)
    
    if end_time == []:
        # pattern_end_crash = "<(.*)> ERROR: $3#SCRIPT ERROR File: =C, Function: _ERRORMESSAGE.*"
        # end_time = findall(pattern_end_crash, log_data)
        end_time = frags[-1][0] # get the last frag
        end_session = end_time
    else:
        end_time = end_time[0].split(':')
        end_session = start_log.replace(minute=int(end_time[0]), second=int(end_time[1]))
      
    if start_session > end_session:
        old_hour = end_session.hour
        end_session.replace(hour=old_hour+1)

    return (start_session, end_session)


def write_frag_csv_file(file_csv, frags):
    """
    Waypoint 9: Create Frag History CSV File
    ---
    @param {str} file_csv: path of new csv file
    @param {list(tuple)} frags: infomation of each frag(time*, killer*, victim, weapon)
    @return: create csv file
    """
    import csv

    with open(file_csv, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(frags)

    csvFile.close()


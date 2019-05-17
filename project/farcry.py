#!/usr/bin/python3
import json
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
            frag_time = start_time.replace(hour= start_hour + 1, minute=int(frag[0][:2]), second=int(frag[0][3:]))
        line = list(frag)
        line.pop(0) # del time
        line.pop(2) # del with/itself
        if len(frag[-1]) > 0: # del space
            line[-1] = frag[-1][1:]
        line = [frag_time.isoformat()] + line # combine frag
        frags.append(tuple(line)) # add to big frags
    rough_frags.clear()
    return frags


if __name__ == "__main__":
    import json

    log_data = read_log_file("../logs/log02.txt")
    wp2_3 = parse_log_start_time(log_data)
    # print(wp2_3)
    wp4 = parse_match_mode_and_map(log_data)
    # print(wp4, type(wp4))
    wp5_6 = parse_frags(log_data)
    my_json_string = json.dumps(wp5_6, indent = 2, sort_keys=True)
    print(my_json_string)

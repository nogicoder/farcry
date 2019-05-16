#!/usr/bin/python3
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
    Parse this date and time information to determine later the timestamp of each frag.
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
    Finding key word 'Loading level' and retrive index of the word that indicates the mode and the map
    ---
    @param {str} log_data: content of log file
    @return {tuple} (mode, map).

    """
    index = log_data.find('Loading level') + 21
    mode_and_map = log_data[index: index+50].split(' ')
    map = mode_and_map[0][:-1]
    mode = mode_and_map[2]
    
    return (mode, map)


def parse_frags(log_data):
    from re import findall
    
    patterm = "<\d{2}:\d{2}>\s<\w*>\s\w*\skilled\s\w*\swith\s\w*"
    frag = findall(patterm, log_data)
    print(frag)

if __name__ == "__main__":
    log_data = read_log_file("../logs/log09.txt")
    wp2_3 = parse_log_start_time(log_data)
    # print(wp2_3)
    wp4 = parse_match_mode_and_map(log_data)
    # print(wp4, type(wp4))
    parse_frags(log_data)
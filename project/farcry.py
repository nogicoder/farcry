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
    Waypoint 2: Parse Far Cry Engine's Start Time
    ---
    Parse this date and time information to determine later the timestamp of each frag.
    ---
    @param {str} log_data: content of log file
    @return {object} start_time:(datetime.datetime) represent the time the Far Cry engine started to log at.

    """
    import datetime
    month = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9,
    'October': 10, 'November': 11, 'December': 12}

    first_line = log_data.split('\n')[0]
    day = first_line.split(' ')[4:-1]
    time = first_line.split(' ')[-1].split(":")
    start_time = datetime.datetime(int(day[2]), month[day[0]], int(day[1][:-1]), int(time[0]), int(time[1]), int(time[2]), tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400)))

    return start_time


if __name__ == "__main__":
    log_data = read_log_file("../logs/log00.txt")
    # print(len(log_data))
    log_start_time = parse_log_start_time(log_data)
    print(log_start_time.isoformat())
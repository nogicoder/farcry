#!/usr/bin/python3

from stage1 import *  # wp1-9
from stage2 import *  # wp24-25

if __name__ == "__main__":
    import json

    number_log_file = '06'
    log_file_pathname = "../../logs/log" + number_log_file + ".txt"
    csv_file_path = "../csv/log" + number_log_file + ".csv"

    # wp1
    log_data = read_log_file(log_file_pathname)
    # print(len(log_data))

    wp2_3 = parse_log_start_time(log_data)
    # print(wp2_3, type(wp2_3)) # type datetime.datetime

    wp4 = parse_match_mode_and_map(log_data)
    # print(wp4, type(wp4))

    wp5_6 = parse_frags(log_data)
    # print(wp5_6)

    wp7 = prettify_frags(wp5_6)
    # print('\n'.join(wp7))

    wp8 = parse_game_session_start_and_end_times(log_data, wp5_6)
    # print(wp8)

    # wp9
    write_frag_csv_file(csv_file_path, wp5_6)

    # wp10 - wp14: Playing with excel.

    # wp15 - wp20: Build Naive Data Model with Navicat Data Modeler

    # wp21- wp24: Create SQLite Database and identify the relationship

    wp25 = insert_match_to_sqlite('../database/farcry.db',
                                  wp8[0], wp8[1], wp4[0],
                                  wp4[1], wp5_6)
    # print(wp25)

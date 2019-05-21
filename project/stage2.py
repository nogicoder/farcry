def insert_match_to_sqlite(data, start_time, end_time, game_mode, map_name, frags):
    import sqlite3
    conn = sqlite3.connect('farcry.db')
    conn.execute()
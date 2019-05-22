def insert_frags_to_sqlite(connection, match_id, frags):
    """
    Waypoint 26: Insert Match Frags into SQLite
    ---
    Inserts new records into the table match_frag.
    ---
    @param {object} connection: a sqlite3 Connection object
    @param {integer} match_id: the identifier of a match
    @param {list} frags: a list of frags
    """
    import sqlite3

    # get all frag history
    frag_history = []
    for frag in frags:
        frag_stats = [match_id]
        if len(frag) > 2:
            frag_stats += [frag[0], frag[1], frag[2], frag[3]]
        else:
            frag_stats += [frag[0], frag[1], None, None]
        frag_history.append(tuple(frag_stats))
    # insert frag to table
    connection.executemany(
        """
        INSERT INTO match_frag \
        (match_id, frag_time, killer_name, victim_name, weapon_code) \
        VALUES \
        (?, ?, ?, ?, ?)
        """,
        frag_history
        )


def insert_match_to_sqlite(match_file, start_time, end_time, game_mode, map_name, frags):

    """
    Waypoint 25: Insert Game Session Data into SQLite
    ---
    Inserts a new record into the table match with
    the arguments start_time, end_time, game_mode, and map_name
    ---
    @param {str} match_file: the path and name of the Far Cry's
    SQLite database.
    @param {object} start_time: time zone information corresponding
    to the start of the game session.
    @param {object} end_time: time zone information corresponding to
    the end of the game session.
    @param {str} game_mode: ASSAULT or TDM or FFA
    @param {str} map_name: name of the map that was played
    @param {list} frags: a list of tuple of the following form
    (frag_time, killer_name[, victim_name, weapon_code])
    @return {integer} match_id: the identifier of the match that has been
    inserted.
    """
    import sqlite3

    # List of data to insert
    match_info = (start_time, end_time, game_mode, map_name)
    # Connect to database
    match_table = sqlite3.connect(match_file)
    # Insert a row of data
    try:
        with match_table:
            cursor_used = match_table.execute(
                """
                INSERT INTO match \
                (start_time, end_time, game_mode, map_name) \
                VALUES \
                (?, ?, ?, ?)
                """,
                match_info
            )
            match_id = cursor_used.lastrowid
            insert_frags_to_sqlite(match_table, match_id, frags)
            # Return match_id according to created cursor object
            return match_id
    except sqlite3.IntegrityError:
        print("Coudn't add match")
        exit(0)

-- Waypoint 43: Select Matches and Calculate the Number of Players and the Number of Kills and Suicides

SELECT
    match.match_id,
    match.start_time,
    match.end_time,
    player_table.player_count,
    COUNT(match_frag.killer_name) AS kill_suicide_count
FROM
    (
        SELECT
            match_id,
            COUNT(DISTINCT killer_name) AS player_count
        FROM
            (
                SELECT
                    match_id,
                    killer_name
                FROM
                    match_frag
                UNION ALL
                SELECT
                    match_id,
                    victim_name
                FROM
                    match_frag
                WHERE
                    victim_name IS NOT NULL
            )
        GROUP BY
            match_id
    ) player_table
    INNER JOIN match ON match.match_id = player_table.match_id
    INNER JOIN match_frag ON match_frag.match_id = player_table.match_id
GROUP BY
    match.match_id;
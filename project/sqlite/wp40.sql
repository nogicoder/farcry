-- Waypoint 40: Calculate and Order the Total Number of Kills per Player

SELECT
    killer_name AS player_name,
    COUNT(victim_name) AS kill_count
FROM
    match_frag
GROUP BY
    player_name
ORDER BY
    kill_count DESC,
    player_name ASC;
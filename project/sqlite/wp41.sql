-- Waypoint 41: Calculate and Order the Number of Kills per Player and per Match

SELECT
	match_id,
	killer_name AS player_name,
    COUNT(victim_name) AS kill_count
FROM
    match_frag
GROUP BY
    match_id,
	player_name
ORDER BY
	match_id ASC,
    kill_count DESC,
    player_name ASC;
-- Waypoint 38: Calculate and Order the Number of Kills and Suicides per Match

SELECT
	match_id,
    COUNT(killer_name) AS kill_suicide_count
FROM 
    match_frag
GROUP BY
    match_id
ORDER BY
    kill_suicide_count DESC;
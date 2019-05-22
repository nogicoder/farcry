-- Waypoint 36: Calculate the Number of Kills (2)

SELECT 
    COUNT(victim_name) AS kill_count
FROM 
    match_frag;
-- Waypoint 35: Calculate the Number of Kills (1)

SELECT 
    COUNT(*) AS kill_count
FROM 
    match_frag
WHERE 
    victim_name IS NOT NULL;
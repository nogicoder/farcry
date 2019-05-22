-- Waypoint 39: Calculate and Order the Number of Suicides per Match

SELECT
	match_id,
    COUNT(killer_name) AS suicide_count
FROM 
    match_frag
WHERE
    victim_name IS NULL    
GROUP BY
    match_id
ORDER BY
    suicide_count ASC;
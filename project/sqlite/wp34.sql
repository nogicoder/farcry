-- Waypoint 34: Calculate the Number of Suicides

SELECT 
	COUNT(*) AS suicide_count
FROM 
	match_frag
WHERE 
	victim_name IS NULL;
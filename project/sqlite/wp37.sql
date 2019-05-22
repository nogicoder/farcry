SELECT
	match_id,
    COUNT(killer_name) AS kill_suicide_count
FROM 
    match_frag
GROUP BY
    match_id;


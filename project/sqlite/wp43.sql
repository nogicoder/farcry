-- Waypoint 43: Select Matches and Calculate the Number of Players and the Number of Kills and Suicides

SELECT
    match.match_id,
    match.start_time,
    match.end_time   
GROUP BY
    match.match_id;
	
SELECT user_id, event, LEAD(event) OVER (PARTITION BY user_id ORDER BY ts) AS next_event FROM events;

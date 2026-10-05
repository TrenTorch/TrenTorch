SELECT first_name || COALESCE(' ' || last_name, '') AS full_name FROM users;

SELECT name,
       CAST(strftime('%Y', '2024-06-30') AS INTEGER) - CAST(strftime('%Y', birth_date) AS INTEGER)
         - (strftime('%m-%d', '2024-06-30') < strftime('%m-%d', birth_date)) AS age_years,
       CAST(julianday('2024-06-30') - julianday(registered_on) AS INTEGER) AS days_registered
FROM users;

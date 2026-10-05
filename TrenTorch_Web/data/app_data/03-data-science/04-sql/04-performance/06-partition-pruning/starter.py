-- @schema
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    event_date TEXT NOT NULL,
    kind TEXT NOT NULL
);
WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 6000)
INSERT INTO events
SELECT i, i % 300, date('2023-01-01', '+' || (i % 730) || ' days'), CASE i % 3 WHEN 0 THEN 'view' WHEN 1 THEN 'click' ELSE 'buy' END
FROM n;
CREATE INDEX idx_events_date ON events(event_date);
-- @query
-- TODO: Count the events from March 2024 without wrapping event_date in a function, so that SQLite can use
-- idx_events_date to read only that slice of the index.


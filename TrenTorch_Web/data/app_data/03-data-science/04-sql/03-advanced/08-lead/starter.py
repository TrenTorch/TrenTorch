-- @schema
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    event TEXT NOT NULL,
    ts TEXT NOT NULL
);
INSERT INTO events VALUES (1, 1, 'signup',   '2024-01-01 09:00');
INSERT INTO events VALUES (2, 1, 'login',    '2024-01-02 10:00');
INSERT INTO events VALUES (3, 1, 'purchase', '2024-01-03 11:00');
INSERT INTO events VALUES (4, 2, 'signup',   '2024-01-01 12:00');
INSERT INTO events VALUES (5, 2, 'login',    '2024-01-05 08:00');
-- @query
-- TODO: Return user_id, event and next_event (that same user's following event by time, NULL for their last event).


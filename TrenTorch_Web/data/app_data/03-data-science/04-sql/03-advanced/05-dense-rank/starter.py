-- @schema
CREATE TABLE scores (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    score INTEGER NOT NULL
);
INSERT INTO scores VALUES (1, 'Alice', 95);
INSERT INTO scores VALUES (2, 'Bob', 90);
INSERT INTO scores VALUES (3, 'Charlie', 90);
INSERT INTO scores VALUES (4, 'Diana', 85);
INSERT INTO scores VALUES (5, 'Eve', 70);
-- @query
-- TODO: Return name, score and score_rank where the highest score has rank 1 and ties share a rank WITHOUT leaving gaps (1, 2, 2, 3).


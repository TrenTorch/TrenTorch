SELECT name, score, DENSE_RANK() OVER (ORDER BY score DESC) AS score_rank FROM scores;

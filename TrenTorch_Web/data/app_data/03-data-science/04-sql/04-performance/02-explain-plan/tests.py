"""Hidden tests: Reading EXPLAIN QUERY PLAN. Run by the in-browser SQL runner (Submit) and by pytest."""

import re


def test_returns_a_query_plan(sql):
    assert sql.columns[-1] == "detail", "EXPLAIN QUERY PLAN returns the columns id, parent, notused and detail."
    assert len(sql.rows) >= 1, "The plan has at least one step."


def test_explains_the_right_query(sql):
    text = re.sub(r"\s+", " ", sql.query.lower())
    assert "explain query plan" in text, "Start the statement with EXPLAIN QUERY PLAN."
    assert "from orders" in text and "total > 90" in text, "Explain exactly: SELECT * FROM orders WHERE total > 90"


def test_plan_is_a_full_table_scan(sql):
    details = " | ".join(row[-1] for row in sql.rows)
    assert "SCAN" in details and "orders" in details, "There is no index on total, so the plan should be a SCAN of orders. Got: " + details
    assert "SEARCH" not in details, "A SEARCH step means an index is used; there is none for total."

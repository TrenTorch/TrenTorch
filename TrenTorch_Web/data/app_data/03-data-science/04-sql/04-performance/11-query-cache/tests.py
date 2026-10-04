"""Hidden tests: Query Caching with Materialized CTEs. Run by the in-browser SQL runner (Submit) and by pytest."""

import re


def test_uses_a_materialized_cte(sql):
    assert re.search(r"\bAS\s+MATERIALIZED\b", sql.query, re.I), "Define the CTE as WITH name AS MATERIALIZED (...)."


def test_top_customers(sql):
    sql.expect_columns(["customer_id", "spend"])
    sql.expect_rows([
        (128, 2790),
        (355, 2780),
        (182, 2770),
        (9, 2760),
        (409, 2760),
    ], ordered=True)

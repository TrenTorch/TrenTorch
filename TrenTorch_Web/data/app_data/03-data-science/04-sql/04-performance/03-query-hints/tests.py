"""Hidden tests: Query Hints: INDEXED BY. Run by the in-browser SQL runner (Submit) and by pytest."""

import re


def test_forces_the_index(sql):
    text = re.sub(r"\s+", " ", sql.query.lower())
    assert "indexed by idx_orders_created" in text, "Add INDEXED BY idx_orders_created after the table name."


def test_count_is_correct(sql):
    sql.expect_rows([
        (1724,),
    ], ordered=False)


def test_plan_uses_the_forced_index(sql):
    plan = " | ".join(sql.plan())
    assert "idx_orders_created" in plan, "The plan should use idx_orders_created. Plan: " + plan

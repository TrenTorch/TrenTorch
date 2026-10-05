"""Hidden tests: Table Statistics with ANALYZE. Run by the in-browser SQL runner (Submit) and by pytest."""

import re


def test_analyze_was_run(sql):
    assert re.search(r"\banalyze\b", sql.query, re.I), "Run ANALYZE so SQLite collects statistics."


def test_reads_the_statistics_table(sql):
    sql.expect_columns(["tbl", "idx", "stat"])
    sql.expect_rows([
        ('orders', 'idx_orders_customer', '5000 10'),
        ('orders', 'idx_orders_status', '5000 1250'),
    ], ordered=True)

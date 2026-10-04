"""Hidden tests: Schema Introspection with PRAGMA. Run by the in-browser SQL runner (Submit) and by pytest."""

import re


def test_returns_the_column_description(sql):
    sql.expect_columns(["name", "type", "notnull", "pk"])
    sql.expect_rows([
        ('id', 'INTEGER', 0, 1),
        ('customer_id', 'INTEGER', 1, 0),
        ('status', 'TEXT', 1, 0),
        ('total', 'INTEGER', 1, 0),
        ('created_on', 'TEXT', 1, 0),
    ], ordered=False)


def test_reads_the_pragma_not_hard_coded_values(sql):
    assert re.search(r"pragma_table_info", sql.query, re.I), "Read the data from pragma_table_info('orders')."

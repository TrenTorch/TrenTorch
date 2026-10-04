"""Hidden tests: Materialized Views (Emulated in SQLite). Run by the in-browser SQL runner (Submit) and by pytest."""


def test_summary_table_exists(sql):
    assert sql.table_exists("sales_by_region"), "Create a table named sales_by_region (CREATE TABLE ... AS SELECT ...)."


def test_summary_has_the_right_columns_and_rows(sql):
    sql.expect_columns(["region", "total_amount", "order_count"])
    sql.expect_rows([
        ('East', 52500, 500),
        ('North', 51500, 500),
        ('South', 52000, 500),
        ('West', 53000, 500),
    ], ordered=True)


def test_summary_is_a_stored_snapshot(sql):
    before = sql.run("SELECT total_amount FROM sales_by_region WHERE region = 'North'")
    sql.run("INSERT INTO sales VALUES (99999, 'North', 'x', 1000)")
    after = sql.run("SELECT total_amount FROM sales_by_region WHERE region = 'North'")
    assert before == after, "The summary must be stored data (a table), not a view that recomputes on every read."

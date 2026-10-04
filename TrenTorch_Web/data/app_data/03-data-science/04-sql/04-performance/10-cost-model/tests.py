"""Hidden tests: A Tiny Cost Model: Selectivity. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_cost_table(sql):
    sql.expect_columns(["status", "row_count", "selectivity", "use_index"])
    sql.expect_rows([
        ('new', 500, 0.1, 1),
        ('paid', 3000, 0.6, 0),
        ('returned', 500, 0.1, 1),
        ('shipped', 1000, 0.2, 0),
    ], ordered=True)


def test_decision_rule_is_selectivity_below_015(sql):
    by_status = {row[0]: row for row in sql.rows}
    assert by_status["paid"][3] == 0, "paid matches 60% of the table: a scan is cheaper than an index."
    assert by_status["returned"][3] == 1, "returned matches only 10% of the table: an index lookup wins."


def test_works_on_different_data(sql):
    other = sql.with_data("""
INSERT INTO orders VALUES (9001, 1, 'returned', 50, '2024-01-01'); INSERT INTO orders VALUES (9002, 1, 'cancelled', 50, '2024-01-01');
""")
    other.expect_rows([
        ('cancelled', 1, 0.0, 1),
        ('new', 500, 0.1, 1),
        ('paid', 3000, 0.6, 0),
        ('returned', 501, 0.1, 1),
        ('shipped', 1000, 0.2, 0),
    ], ordered=True)

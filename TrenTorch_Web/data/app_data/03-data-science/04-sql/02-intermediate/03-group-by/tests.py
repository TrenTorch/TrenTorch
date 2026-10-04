"""Hidden tests: GROUP BY Aggregation. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['user_id', 'order_count'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        (1, 2),
        (2, 1),
        (3, 3),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO orders VALUES (7, 4, 'Pen', 2); INSERT INTO orders VALUES (8, 2, 'Pad', 5);
""")
    other.expect_rows([
        (1, 2),
        (2, 2),
        (3, 3),
        (4, 1),
    ], ordered=False)

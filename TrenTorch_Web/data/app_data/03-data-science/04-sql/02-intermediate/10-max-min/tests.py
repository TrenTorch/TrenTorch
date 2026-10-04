"""Hidden tests: MAX and MIN. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['category', 'max_price', 'min_price'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        ('Electronics', 900, 20),
        ('Furniture', 150, 30),
        ('Stationery', 2, 2),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO products VALUES (7, 'Notebook', 'Stationery', 5); INSERT INTO products VALUES (8, 'Phone', 'Electronics', 600);
""")
    other.expect_rows([
        ('Electronics', 900, 20),
        ('Furniture', 150, 30),
        ('Stationery', 5, 2),
    ], ordered=False)

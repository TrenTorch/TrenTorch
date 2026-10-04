"""Hidden tests: INNER JOIN Combining Tables. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['user_id', 'product', 'name'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        (1, 'Laptop', 'Alice'),
        (1, 'Mouse', 'Alice'),
        (2, 'Desk', 'Bob'),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO users VALUES (4, 'Dan'); INSERT INTO orders VALUES (5, 4, 'Chair');
""")
    other.expect_rows([
        (1, 'Laptop', 'Alice'),
        (1, 'Mouse', 'Alice'),
        (2, 'Desk', 'Bob'),
        (4, 'Chair', 'Dan'),
    ], ordered=False)

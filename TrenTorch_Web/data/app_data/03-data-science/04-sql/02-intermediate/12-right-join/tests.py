"""Hidden tests: RIGHT JOIN. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['order_id', 'name'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        (1, 'Alice'),
        (2, 'Alice'),
        (3, 'Bob'),
        (4, None),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO users VALUES (4, 'Dan'); INSERT INTO orders VALUES (5, 4, 'Chair'); INSERT INTO orders VALUES (6, 77, 'Phantom');
""")
    other.expect_rows([
        (1, 'Alice'),
        (2, 'Alice'),
        (3, 'Bob'),
        (5, 'Dan'),
        (4, None),
        (6, None),
    ], ordered=False)

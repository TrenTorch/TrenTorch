"""Hidden tests: LEFT JOIN Preserving Left Table. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['id', 'name', 'order_count'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        (1, 'Alice', 2),
        (2, 'Bob', 1),
        (3, 'Cara', 0),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO users VALUES (4, 'Dan'); INSERT INTO orders VALUES (5, 3, 'Chair'); INSERT INTO orders VALUES (6, 3, 'Lamp');
""")
    other.expect_rows([
        (1, 'Alice', 2),
        (2, 'Bob', 1),
        (3, 'Cara', 2),
        (4, 'Dan', 0),
    ], ordered=False)

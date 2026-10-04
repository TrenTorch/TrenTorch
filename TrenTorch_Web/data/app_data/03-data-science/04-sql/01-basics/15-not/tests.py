"""Hidden tests: NOT Negation. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['id', 'name', 'age'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        (1, 'Alice', 25),
        (2, 'Bob', 30),
        (5, 'Dana', 41),
        (6, 'Eli', 19),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO users VALUES (7, 'Cleo', 50); INSERT INTO users VALUES (8, 'Fred', 44);
""")
    other.expect_rows([
        (1, 'Alice', 25),
        (2, 'Bob', 30),
        (5, 'Dana', 41),
        (6, 'Eli', 19),
        (8, 'Fred', 44),
    ], ordered=False)

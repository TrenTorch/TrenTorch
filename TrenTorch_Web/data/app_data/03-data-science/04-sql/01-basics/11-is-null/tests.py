"""Hidden tests: IS NULL Checking. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['id', 'name', 'email'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        (2, 'Bob', None),
        (4, 'Dan', None),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO users VALUES (6, 'Fay', NULL); INSERT INTO users VALUES (7, 'Gus', '');
""")
    other.expect_rows([
        (2, 'Bob', None),
        (4, 'Dan', None),
        (6, 'Fay', None),
    ], ordered=False)

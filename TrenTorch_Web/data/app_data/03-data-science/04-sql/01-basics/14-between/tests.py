"""Hidden tests: BETWEEN Range Filtering. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['id', 'name', 'age'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        (2, 'Bob', 30),
        (3, 'Charlie', 35),
        (4, 'Diana', 40),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO users VALUES (7, 'Gina', 30); INSERT INTO users VALUES (8, 'Hari', 40); INSERT INTO users VALUES (9, 'Ivy', 31);
""")
    other.expect_rows([
        (2, 'Bob', 30),
        (3, 'Charlie', 35),
        (4, 'Diana', 40),
        (7, 'Gina', 30),
        (8, 'Hari', 40),
        (9, 'Ivy', 31),
    ], ordered=False)

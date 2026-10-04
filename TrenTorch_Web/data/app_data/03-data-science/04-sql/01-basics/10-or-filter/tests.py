"""Hidden tests: OR Alternative Filtering. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['id', 'name', 'age'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        (1, 'Alice', 12),
        (2, 'Bob', 17),
        (5, 'Eve', 66),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO users VALUES (7, 'Gina', 90); INSERT INTO users VALUES (8, 'Hari', 18); INSERT INTO users VALUES (9, 'Ivy', 5);
""")
    other.expect_rows([
        (1, 'Alice', 12),
        (2, 'Bob', 17),
        (5, 'Eve', 66),
        (7, 'Gina', 90),
        (9, 'Ivy', 5),
    ], ordered=False)

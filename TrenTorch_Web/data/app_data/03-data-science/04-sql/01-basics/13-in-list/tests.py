"""Hidden tests: IN List Matching. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['id', 'name', 'age'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        (1, 'Alice', 12),
        (3, 'Charlie', 16),
        (5, 'Eve', 66),
        (7, 'Gina', 12),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO users VALUES (8, 'Hari', 66); INSERT INTO users VALUES (9, 'Ivy', 15);
""")
    other.expect_rows([
        (1, 'Alice', 12),
        (3, 'Charlie', 16),
        (5, 'Eve', 66),
        (7, 'Gina', 12),
        (8, 'Hari', 66),
    ], ordered=False)

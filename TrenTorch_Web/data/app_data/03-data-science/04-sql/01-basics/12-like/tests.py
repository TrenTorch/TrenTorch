"""Hidden tests: LIKE Pattern Matching. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['id', 'name', 'email'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        (1, 'Alice', 'alice@example.com'),
        (4, 'Dave', 'dave@EXAMPLE.COM'),
        (6, 'Frank', 'frank@example.com'),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO users VALUES (7, 'Gina', 'gina@example.com'); INSERT INTO users VALUES (8, 'Hari', 'hari@example.org');
""")
    other.expect_rows([
        (1, 'Alice', 'alice@example.com'),
        (4, 'Dave', 'dave@EXAMPLE.COM'),
        (6, 'Frank', 'frank@example.com'),
        (7, 'Gina', 'gina@example.com'),
    ], ordered=False)

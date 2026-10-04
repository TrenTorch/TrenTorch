"""Hidden tests: WHERE Filtering. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['id', 'name', 'email', 'age'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        (1, 'Alice', 'alice@example.com', 25),
        (3, 'Charlie', 'charlie@example.com', 18),
        (5, 'Eve', 'eve@example.com', 42),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO users VALUES (6, 'Frank', 'frank@example.com', 18); INSERT INTO users VALUES (7, 'Gina', 'gina@example.com', 9);
""")
    other.expect_rows([
        (1, 'Alice', 'alice@example.com', 25),
        (3, 'Charlie', 'charlie@example.com', 18),
        (5, 'Eve', 'eve@example.com', 42),
        (6, 'Frank', 'frank@example.com', 18),
    ], ordered=False)

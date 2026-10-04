"""Hidden tests: SELECT Specific Columns. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['name', 'email'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        ('Alice', 'alice@example.com'),
        ('Bob', 'bob@example.com'),
        ('Charlie', 'charlie@example.com'),
        ('Diana', 'diana@example.com'),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO users VALUES (5, 'Eve', 'eve@example.com', 41);
""")
    other.expect_rows([
        ('Alice', 'alice@example.com'),
        ('Bob', 'bob@example.com'),
        ('Charlie', 'charlie@example.com'),
        ('Diana', 'diana@example.com'),
        ('Eve', 'eve@example.com'),
    ], ordered=False)

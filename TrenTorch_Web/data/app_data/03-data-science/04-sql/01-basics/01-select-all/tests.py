"""Hidden tests: SELECT All Rows. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['id', 'name', 'email', 'age'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        (1, 'Alice', 'alice@example.com', 25),
        (2, 'Bob', 'bob@example.com', 30),
        (3, 'Charlie', 'charlie@example.com', 35),
        (4, 'Diana', 'diana@example.com', 17),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO users VALUES (5, 'Eve', 'eve@example.com', 41);
""")
    other.expect_rows([
        (1, 'Alice', 'alice@example.com', 25),
        (2, 'Bob', 'bob@example.com', 30),
        (3, 'Charlie', 'charlie@example.com', 35),
        (4, 'Diana', 'diana@example.com', 17),
        (5, 'Eve', 'eve@example.com', 41),
    ], ordered=False)

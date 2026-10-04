"""Hidden tests: ORDER BY Sorting. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['id', 'name', 'email', 'age'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        (3, 'Eve', 'eve@example.com', 41),
        (1, 'Charlie', 'charlie@example.com', 35),
        (4, 'Bob', 'bob@example.com', 30),
        (2, 'Alice', 'alice@example.com', 25),
    ], ordered=True)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO users VALUES (5, 'Zed', 'zed@example.com', 99); INSERT INTO users VALUES (6, 'Kim', 'kim@example.com', 3);
""")
    other.expect_rows([
        (5, 'Zed', 'zed@example.com', 99),
        (3, 'Eve', 'eve@example.com', 41),
        (1, 'Charlie', 'charlie@example.com', 35),
        (4, 'Bob', 'bob@example.com', 30),
        (2, 'Alice', 'alice@example.com', 25),
        (6, 'Kim', 'kim@example.com', 3),
    ], ordered=True)

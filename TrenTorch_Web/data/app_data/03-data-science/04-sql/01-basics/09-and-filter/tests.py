"""Hidden tests: AND Compound Filtering. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['id', 'name', 'email', 'age'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        (1, 'Alice', 'alice@example.com', 25),
        (4, 'Anna', 'anna@example.com', 40),
        (5, 'Aaron', 'aaron@example.com', 18),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO users VALUES (7, 'Amy', 'amy@example.com', 19); INSERT INTO users VALUES (8, 'Alan', 'alan@example.com', 10);
""")
    other.expect_rows([
        (1, 'Alice', 'alice@example.com', 25),
        (4, 'Anna', 'anna@example.com', 40),
        (5, 'Aaron', 'aaron@example.com', 18),
        (7, 'Amy', 'amy@example.com', 19),
    ], ordered=False)

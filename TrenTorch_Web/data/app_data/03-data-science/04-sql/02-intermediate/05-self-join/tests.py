"""Hidden tests: SELF JOIN. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['employee', 'manager'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        ('Bob', 'Alice'),
        ('Charlie', 'Alice'),
        ('Diana', 'Bob'),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO employees VALUES (5, 'Eve', 3); INSERT INTO employees VALUES (6, 'Frank', NULL);
""")
    other.expect_rows([
        ('Bob', 'Alice'),
        ('Charlie', 'Alice'),
        ('Diana', 'Bob'),
        ('Eve', 'Charlie'),
    ], ordered=False)

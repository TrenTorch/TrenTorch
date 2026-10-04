"""Hidden tests: Recursive CTE: Hierarchical Data. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['id', 'name', 'depth'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        (2, 'Bob', 1),
        (3, 'Charlie', 1),
        (4, 'Diana', 2),
        (6, 'Frank', 2),
        (5, 'Eve', 3),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO employees VALUES (8, 'Hari', 5); INSERT INTO employees VALUES (9, 'Ivy', 7);
""")
    other.expect_rows([
        (2, 'Bob', 1),
        (3, 'Charlie', 1),
        (4, 'Diana', 2),
        (6, 'Frank', 2),
        (5, 'Eve', 3),
        (8, 'Hari', 4),
    ], ordered=False)

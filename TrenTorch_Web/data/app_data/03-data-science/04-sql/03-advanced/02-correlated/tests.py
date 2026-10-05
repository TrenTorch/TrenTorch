"""Hidden tests: Correlated Subqueries: Row-by-Row. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['name', 'department', 'salary'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        ('Charlie', 'Engineering', 90000),
        ('Eve', 'Sales', 44000),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO employees VALUES (7, 'Gina', 'HR', 70000); INSERT INTO employees VALUES (8, 'Hari', 'Sales', 30000);
""")
    other.expect_rows([
        ('Charlie', 'Engineering', 90000),
        ('Diana', 'Sales', 40000),
        ('Eve', 'Sales', 44000),
        ('Gina', 'HR', 70000),
    ], ordered=False)

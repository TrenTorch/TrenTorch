"""Hidden tests: RANK: Window Function with Gaps. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['name', 'region', 'age', 'age_rank'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        ('Alice', 'North', 40, 1),
        ('Bob', 'North', 35, 2),
        ('Charlie', 'North', 35, 2),
        ('Diana', 'North', 28, 4),
        ('Eve', 'South', 50, 1),
        ('Frank', 'South', 31, 2),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO users VALUES (7, 'Gina', 'South', 50); INSERT INTO users VALUES (8, 'Hari', 'West', 22);
""")
    other.expect_rows([
        ('Alice', 'North', 40, 1),
        ('Bob', 'North', 35, 2),
        ('Charlie', 'North', 35, 2),
        ('Diana', 'North', 28, 4),
        ('Eve', 'South', 50, 1),
        ('Gina', 'South', 50, 1),
        ('Frank', 'South', 31, 3),
        ('Hari', 'West', 22, 1),
    ], ordered=False)

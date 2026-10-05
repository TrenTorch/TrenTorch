"""Hidden tests: DENSE_RANK: Window Function without Gaps. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['name', 'score', 'score_rank'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        ('Alice', 95, 1),
        ('Bob', 90, 2),
        ('Charlie', 90, 2),
        ('Diana', 85, 3),
        ('Eve', 70, 4),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO scores VALUES (6, 'Frank', 95); INSERT INTO scores VALUES (7, 'Gina', 60);
""")
    other.expect_rows([
        ('Alice', 95, 1),
        ('Frank', 95, 1),
        ('Bob', 90, 2),
        ('Charlie', 90, 2),
        ('Diana', 85, 3),
        ('Eve', 70, 4),
        ('Gina', 60, 5),
    ], ordered=False)

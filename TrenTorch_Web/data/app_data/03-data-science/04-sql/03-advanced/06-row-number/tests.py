"""Hidden tests: ROW_NUMBER: Unique Sequential Numbering. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['name', 'age', 'row_num'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        ('Diana', 22, 1),
        ('Bob', 25, 2),
        ('Alice', 30, 3),
        ('Charlie', 30, 4),
        ('Eve', 41, 5),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO users VALUES (6, 'Frank', 22); INSERT INTO users VALUES (7, 'Gina', 18);
""")
    other.expect_rows([
        ('Gina', 18, 1),
        ('Diana', 22, 2),
        ('Frank', 22, 3),
        ('Bob', 25, 4),
        ('Alice', 30, 5),
        ('Charlie', 30, 6),
        ('Eve', 41, 7),
    ], ordered=False)

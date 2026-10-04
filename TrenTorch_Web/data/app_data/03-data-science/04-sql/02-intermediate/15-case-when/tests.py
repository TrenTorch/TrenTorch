"""Hidden tests: CASE WHEN. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['name', 'age_group'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        ('Alice', 'minor'),
        ('Bob', 'minor'),
        ('Charlie', 'adult'),
        ('Diana', 'adult'),
        ('Eve', 'senior'),
        ('Frank', 'adult'),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO users VALUES (7, 'Gina', 90); INSERT INTO users VALUES (8, 'Hari', 3);
""")
    other.expect_rows([
        ('Alice', 'minor'),
        ('Bob', 'minor'),
        ('Charlie', 'adult'),
        ('Diana', 'adult'),
        ('Eve', 'senior'),
        ('Frank', 'adult'),
        ('Gina', 'senior'),
        ('Hari', 'minor'),
    ], ordered=False)

"""Hidden tests: Date Functions: Time Calculations. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['name', 'age_years', 'days_registered'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        ('Alice', 34, 181),
        ('Bob', 23, 29),
        ('Charlie', 39, 366),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO users VALUES (4, 'Dan', '2024-01-01', '2024-06-29'); INSERT INTO users VALUES (5, 'Eve', '1950-07-01', '2020-02-29');
""")
    other.expect_rows([
        ('Alice', 34, 181),
        ('Bob', 23, 29),
        ('Charlie', 39, 366),
        ('Dan', 0, 1),
        ('Eve', 73, 1583),
    ], ordered=False)

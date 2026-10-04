"""Hidden tests: SUM with GROUP BY. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['region', 'total_revenue'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        ('East', 80),
        ('North', 275),
        ('South', 300),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO sales VALUES (7, 'West', 500); INSERT INTO sales VALUES (8, 'East', 20);
""")
    other.expect_rows([
        ('East', 100),
        ('North', 275),
        ('South', 300),
        ('West', 500),
    ], ordered=False)

"""Hidden tests: LAG: Access Previous Row. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['month', 'revenue', 'prev_revenue'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        ('2024-01', 1000, None),
        ('2024-02', 1200, 1000),
        ('2024-03', 900, 1200),
        ('2024-04', 1500, 900),
    ], ordered=True)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO monthly_sales VALUES ('2024-05', 1100); INSERT INTO monthly_sales VALUES ('2023-12', 800);
""")
    other.expect_rows([
        ('2023-12', 800, None),
        ('2024-01', 1000, 800),
        ('2024-02', 1200, 1000),
        ('2024-03', 900, 1200),
        ('2024-04', 1500, 900),
        ('2024-05', 1100, 1500),
    ], ordered=True)

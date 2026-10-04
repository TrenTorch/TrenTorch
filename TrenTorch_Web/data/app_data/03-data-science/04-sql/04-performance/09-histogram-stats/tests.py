"""Hidden tests: Value Distributions (Histograms). Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_distribution(sql):
    sql.expect_columns(["status", "row_count", "pct"])
    sql.expect_rows([
        ('paid', 3000, 60.0),
        ('shipped', 1000, 20.0),
        ('new', 500, 10.0),
        ('returned', 500, 10.0),
    ], ordered=True)


def test_percentages_add_up(sql):
    assert abs(sum(row[2] for row in sql.rows) - 100.0) < 0.5, "The percentages should add up to about 100."


def test_works_on_different_data(sql):
    other = sql.with_data("""
INSERT INTO orders VALUES (9001, 1, 'returned', 50, '2024-01-01'); INSERT INTO orders VALUES (9002, 1, 'returned', 50, '2024-01-01'); INSERT INTO orders VALUES (9003, 1, 'cancelled', 50, '2024-01-01');
""")
    other.expect_rows([
        ('paid', 3000, 60.0),
        ('shipped', 1000, 20.0),
        ('returned', 502, 10.0),
        ('new', 500, 10.0),
        ('cancelled', 1, 0.0),
    ], ordered=True)

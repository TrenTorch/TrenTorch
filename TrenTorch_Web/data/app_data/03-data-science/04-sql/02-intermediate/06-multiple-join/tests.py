"""Hidden tests: MULTIPLE JOIN. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['user_name', 'product_name', 'quantity'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        ('Alice', 'Laptop', 1),
        ('Alice', 'Mouse', 3),
        ('Bob', 'Desk', 2),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO orders VALUES (4, 2, 1, 5);
""")
    other.expect_rows([
        ('Alice', 'Laptop', 1),
        ('Alice', 'Mouse', 3),
        ('Bob', 'Desk', 2),
        ('Bob', 'Laptop', 5),
    ], ordered=False)

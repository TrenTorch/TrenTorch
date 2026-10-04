"""Hidden tests: DISTINCT COUNT. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['customer_count'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        (3,),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO orders VALUES (7, 4, 'Pen'); INSERT INTO orders VALUES (8, 1, 'Pad'); INSERT INTO orders VALUES (9, 5, 'Ink');
""")
    other.expect_rows([
        (5,),
    ], ordered=False)

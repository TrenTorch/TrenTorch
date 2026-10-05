"""Hidden tests: NTH Highest Value. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_number_of_columns(sql):
    sql.expect_column_count(1)


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        (30,),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO users VALUES (6, 'Frank', 55); INSERT INTO users VALUES (7, 'Gina', 55);
""")
    other.expect_rows([
        (40,),
    ], ordered=False)

"""Hidden tests: DISTINCT Deduplication. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['city'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        ('Pune',),
        ('Mumbai',),
        ('Delhi',),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO users VALUES (7, 'Gina', 'Chennai'); INSERT INTO users VALUES (8, 'Hari', 'Delhi');
""")
    other.expect_rows([
        ('Pune',),
        ('Mumbai',),
        ('Delhi',),
        ('Chennai',),
    ], ordered=False)

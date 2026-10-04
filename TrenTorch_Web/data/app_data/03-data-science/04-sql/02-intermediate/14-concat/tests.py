"""Hidden tests: String CONCAT. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['full_name'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        ('John Doe',),
        ('Jane Smith',),
        ('Prince',),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO users VALUES (4, 'Cher', NULL); INSERT INTO users VALUES (5, 'Ada', 'Lovelace');
""")
    other.expect_rows([
        ('John Doe',),
        ('Jane Smith',),
        ('Prince',),
        ('Cher',),
        ('Ada Lovelace',),
    ], ordered=False)

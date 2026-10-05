"""Hidden tests: CROSS JOIN. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['color', 'size'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        ('Red', 'Small'),
        ('Red', 'Medium'),
        ('Red', 'Large'),
        ('Blue', 'Small'),
        ('Blue', 'Medium'),
        ('Blue', 'Large'),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO colors VALUES (3, 'Green'); INSERT INTO sizes VALUES (4, 'XL');
""")
    other.expect_rows([
        ('Red', 'Small'),
        ('Red', 'Medium'),
        ('Red', 'Large'),
        ('Red', 'XL'),
        ('Blue', 'Small'),
        ('Blue', 'Medium'),
        ('Blue', 'Large'),
        ('Blue', 'XL'),
        ('Green', 'Small'),
        ('Green', 'Medium'),
        ('Green', 'Large'),
        ('Green', 'XL'),
    ], ordered=False)

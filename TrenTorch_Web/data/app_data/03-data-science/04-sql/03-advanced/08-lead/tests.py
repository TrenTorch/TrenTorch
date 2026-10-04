"""Hidden tests: LEAD: Access Next Row. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['user_id', 'event', 'next_event'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        (1, 'signup', 'login'),
        (1, 'login', 'purchase'),
        (1, 'purchase', None),
        (2, 'signup', 'login'),
        (2, 'login', None),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO events VALUES (6, 3, 'signup', '2024-02-01 09:00'); INSERT INTO events VALUES (7, 2, 'logout', '2024-01-06 08:00');
""")
    other.expect_rows([
        (1, 'signup', 'login'),
        (1, 'login', 'purchase'),
        (1, 'purchase', None),
        (2, 'signup', 'login'),
        (2, 'login', 'logout'),
        (2, 'logout', None),
        (3, 'signup', None),
    ], ordered=False)

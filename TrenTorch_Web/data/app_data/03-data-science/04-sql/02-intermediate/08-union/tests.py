"""Hidden tests: UNION Combining Queries. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_returns_the_right_columns(sql):
    sql.expect_columns(['id', 'name', 'email'])


def test_returns_the_expected_rows(sql):
    sql.expect_rows([
        (1, 'Alice', 'alice@example.com'),
        (2, 'Bob', 'bob@example.com'),
        (3, 'Cara', 'cara@example.com'),
        (7, 'Gus', 'gus@example.com'),
    ], ordered=False)


def test_works_on_different_data(sql):
    # Hidden rows: a query that hard-codes the visible answer fails here.
    other = sql.with_data("""
INSERT INTO archive_users VALUES (1, 'Alice', 'alice@example.com'); INSERT INTO archive_users VALUES (8, 'Hari', 'hari@example.com');
""")
    other.expect_rows([
        (1, 'Alice', 'alice@example.com'),
        (2, 'Bob', 'bob@example.com'),
        (3, 'Cara', 'cara@example.com'),
        (7, 'Gus', 'gus@example.com'),
        (8, 'Hari', 'hari@example.com'),
    ], ordered=False)

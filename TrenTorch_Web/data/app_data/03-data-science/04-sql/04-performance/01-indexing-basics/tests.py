"""Hidden tests: Indexes: Turning Scans into Searches. Run by the in-browser SQL runner (Submit) and by pytest."""


def test_index_exists_on_customer_id(sql):
    found = sql.index_columns("orders")
    assert "idx_orders_customer" in found, "Create an index named idx_orders_customer on the orders table."
    assert found["idx_orders_customer"] == ["customer_id"], "The index should cover exactly the column customer_id."


def test_lookup_returns_the_customers_orders(sql):
    sql.expect_rows([
        (41, 42, 'new', 327, '2024-02-11'),
        (541, 42, 'new', 27, '2024-06-24'),
        (1041, 42, 'new', 127, '2024-11-05'),
        (1541, 42, 'new', 227, '2024-03-18'),
        (2041, 42, 'new', 327, '2024-07-30'),
        (2541, 42, 'new', 27, '2024-12-11'),
        (3041, 42, 'new', 127, '2024-04-23'),
        (3541, 42, 'new', 227, '2024-09-04'),
        (4041, 42, 'new', 327, '2024-01-16'),
        (4541, 42, 'new', 27, '2024-05-29'),
    ], ordered=False)


def test_lookup_uses_the_index(sql):
    plan = " | ".join(sql.plan())
    assert "idx_orders_customer" in plan and "SEARCH" in plan, (
        "SQLite still scans the whole table. Plan: " + plan
    )

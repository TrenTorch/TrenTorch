import pandas as pd


def orders_with_customers(customers: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    """
    Inner join on orders.customer_id == customers.id. Columns: order_id,
    customer_id, name, amount. Sorted by order_id, fresh 0..n-1 index.
    """
    # TODO: Inner-join and tidy the result.
    pass


def customer_totals(customers: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    """
    One row per customer: id, name, n_orders (int), total (sum of amount).
    No orders -> n_orders 0, total 0.0. Sorted by id, fresh index.
    """
    # TODO: Summarise the orders, then left-join and fill the gaps.
    pass


def customers_without_orders(customers: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    """Rows of customers whose id appears in no order, original order, fresh index."""
    # TODO: Anti-join.
    pass


def safe_merge(left: pd.DataFrame, right: pd.DataFrame, key: str) -> pd.DataFrame:
    """
    Left join on `key`, keeping left's row order, fresh index. Raises
    ValueError if `right` repeats a key value.
    """
    # TODO: Left-join with the relationship checked.
    pass

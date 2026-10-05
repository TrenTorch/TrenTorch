import pandas as pd


def orders_with_customers(customers: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    joined = orders.merge(customers, left_on="customer_id", right_on="id", how="inner")
    out = joined[["order_id", "customer_id", "name", "amount"]]
    return out.sort_values("order_id", kind="mergesort").reset_index(drop=True)


def customer_totals(customers: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    per_customer = (
        orders.groupby("customer_id")["amount"].agg(n_orders="count", total="sum").reset_index()
    )
    out = customers[["id", "name"]].merge(per_customer, left_on="id", right_on="customer_id", how="left")
    out["n_orders"] = out["n_orders"].fillna(0).astype(int)
    out["total"] = out["total"].fillna(0.0).astype(float)
    out = out[["id", "name", "n_orders", "total"]]
    return out.sort_values("id", kind="mergesort").reset_index(drop=True)


def customers_without_orders(customers: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    return customers[~customers["id"].isin(orders["customer_id"])].reset_index(drop=True)


def safe_merge(left: pd.DataFrame, right: pd.DataFrame, key: str) -> pd.DataFrame:
    return left.merge(right, on=key, how="left", validate="m:1").reset_index(drop=True)

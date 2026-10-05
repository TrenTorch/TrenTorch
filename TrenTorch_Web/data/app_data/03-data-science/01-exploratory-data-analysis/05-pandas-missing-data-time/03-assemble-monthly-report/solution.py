import pandas as pd


def monthly_report(orders: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    columns = ["orders", "revenue", "avg_order_value", "growth_pct", "top_region"]
    o = orders.copy()
    o["date"] = pd.to_datetime(o["order_date"], format="%Y-%m-%d", errors="coerce")
    o = o.dropna(subset=["date"])
    o = o.merge(customers[["id", "region"]], left_on="customer_id", right_on="id", how="inner")
    if o.empty:
        return pd.DataFrame({c: [] for c in columns}, index=pd.DatetimeIndex([], name="month"))
    o["month"] = o["date"].dt.to_period("M").dt.to_timestamp()
    months = pd.date_range(o["month"].min(), o["month"].max(), freq="MS", name="month")
    g = o.groupby("month")["amount"].agg(orders="count", revenue="sum").reindex(months)
    g["orders"] = g["orders"].fillna(0).astype(int)
    g["revenue"] = g["revenue"].fillna(0.0).astype(float)
    g["avg_order_value"] = g["revenue"] / g["orders"].where(g["orders"] > 0)
    previous = g["revenue"].shift(1)
    g["growth_pct"] = 100.0 * (g["revenue"] - previous) / previous.where(previous > 0)
    by_region = o.groupby(["month", "region"])["amount"].sum().reset_index()
    by_region = by_region.sort_values(["month", "amount", "region"], ascending=[True, False, True])
    top = by_region.groupby("month").head(1).set_index("month")["region"]
    g["top_region"] = top.reindex(months).astype(object).where(top.reindex(months).notna(), None)
    return g[columns]

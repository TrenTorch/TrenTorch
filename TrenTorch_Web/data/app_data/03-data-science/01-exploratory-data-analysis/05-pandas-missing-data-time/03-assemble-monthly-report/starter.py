import pandas as pd


def monthly_report(orders: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    """
    One row per month (month start, index named "month"), every month from the
    first to the last valid order. Columns: orders, revenue, avg_order_value,
    growth_pct, top_region. See the Statement for the exact rules.
    """
    # TODO: Parse, join, group by month, fill the calendar, derive the measures.
    pass

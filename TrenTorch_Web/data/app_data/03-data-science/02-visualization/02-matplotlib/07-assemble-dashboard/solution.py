import matplotlib.pyplot as plt
import pandas as pd


def sales_dashboard(df: pd.DataFrame):
    fig, (ax_month, ax_region, ax_amount) = plt.subplots(1, 3, figsize=(15, 4))

    monthly = df.groupby(df["date"].dt.to_period("M"))["amount"].sum().sort_index()
    ax_month.plot(monthly.index.to_timestamp(), monthly.to_numpy())
    ax_month.set_title("Revenue by month")
    ax_month.set_xlabel("Month")
    ax_month.set_ylabel("Revenue")

    by_region = df.groupby("region")["amount"].sum().sort_index()
    by_region = by_region.sort_values(ascending=False, kind="mergesort")
    ax_region.bar(range(len(by_region)), by_region.to_numpy())
    ax_region.set_xticks(range(len(by_region)))
    ax_region.set_xticklabels(by_region.index.tolist())
    ax_region.set_title("Revenue by region")
    ax_region.set_xlabel("Region")
    ax_region.set_ylabel("Revenue")

    ax_amount.hist(df["amount"], bins=5)
    ax_amount.set_title("Order amounts")
    ax_amount.set_xlabel("Amount")
    ax_amount.set_ylabel("Orders")

    fig.suptitle("Sales dashboard")
    fig.tight_layout()
    return fig

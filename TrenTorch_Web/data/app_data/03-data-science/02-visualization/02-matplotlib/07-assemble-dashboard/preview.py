import numpy as np
import pandas as pd

rng = np.random.default_rng(2)
n = 120
df = pd.DataFrame(
    {
        "date": pd.Timestamp("2024-01-01") + pd.to_timedelta(rng.integers(0, 150, n), unit="D"),
        "region": rng.choice(["north", "south", "east", "west"], n),
        "amount": rng.gamma(2.0, 30.0, n).round(2),
    }
)
show(sales_dashboard(df))

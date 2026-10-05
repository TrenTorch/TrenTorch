import numpy as np
import pandas as pd

rng = np.random.default_rng(4)
df = pd.DataFrame(
    {
        "g": np.tile(["north", "south", "east"], 40),
        "kind": np.tile(["p", "q", "r", "s"], 30),
        "v": rng.normal(size=120),
        "w": rng.normal(size=120),
        "z": rng.normal(size=120),
    }
)
show(histograms_by_group(df, "v", "g", ["north", "south", "east"], 8))
show(bars_by_group(df, "kind", "v", "g", ["north", "south", "east"]))
show(pair_scatter(df, ["v", "w", "z"]))

import numpy as np
import pandas as pd

rng = np.random.default_rng(0)
df = pd.DataFrame({"x": rng.normal(size=60), "y": rng.normal(size=60), "g": rng.choice(["a", "b", "c"], 60)})
show(scatter_by_group(df, "x", "y", "g", ["a", "b", "c"]))
show(total_bars(df.assign(v=rng.integers(1, 20, 60)), "g", "v"))
show(histogram_figure(df, "x", 12))
lines = pd.DataFrame({"x": np.tile(np.arange(10), 2), "y": rng.normal(size=20).cumsum(), "g": ["a"] * 10 + ["b"] * 10})
show(lines_by_group(lines, "x", "y", "g"))

import numpy as np
import pandas as pd

x = list(range(1, 11))
show(stacked_panels(x, [v * 1.5 for v in x], [10 - v for v in x], ("Price", "Volume")))
rng = np.random.default_rng(1)
df = pd.DataFrame({"x": rng.normal(size=60), "y": rng.normal(size=60), "region": rng.choice(["north", "west", "east"], 60)})
fig = facet_scatter(df, "x", "y", "region", ["north", "west", "east"])
print("panel titles:", panel_titles(fig))
show(fig)

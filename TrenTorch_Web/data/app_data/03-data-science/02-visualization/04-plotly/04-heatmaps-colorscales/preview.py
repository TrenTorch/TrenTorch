import numpy as np
import pandas as pd

z = [[1.0, 0.2, -0.9], [0.2, 1.0, 0.5], [-0.9, 0.5, 1.0]]
fig = heatmap_figure(z, ["a", "b", "c"], ["a", "b", "c"], "A matrix", -1, 1, "RdBu")
print("strong cells annotated:", annotate_strong_cells(fig, z, ["a", "b", "c"], ["a", "b", "c"], 0.8))
show(fig)
rng = np.random.default_rng(2)
a = rng.normal(size=100)
show(correlation_heatmap(pd.DataFrame({"a": a, "b": 2 * a + rng.normal(size=100), "c": rng.normal(size=100)})))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

rng = np.random.default_rng(2)
points = pd.DataFrame({"x": rng.normal(size=80), "y": rng.normal(size=80), "kind": rng.choice(["cat", "dog", "owl"], 80)})
plt.figure(figsize=(6, 4))
show(scatter_by_group(points, "x", "y", "kind", ["cat", "dog", "owl"]))
runs = pd.DataFrame({"t": np.repeat(np.arange(1, 7), 8), "v": np.repeat(np.arange(1, 7), 8) * 2 + rng.normal(0, 2, 48)})
plt.figure(figsize=(6, 4))
show(mean_line(runs, "t", "v"))
plt.figure(figsize=(6, 4))
show(line_with_band(runs, "t", "v"))

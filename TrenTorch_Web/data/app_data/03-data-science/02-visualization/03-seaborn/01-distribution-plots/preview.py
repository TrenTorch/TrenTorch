import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

rng = np.random.default_rng(0)
df = pd.DataFrame({"x": np.concatenate([rng.normal(0, 1, 150), rng.normal(4, 1, 150)]), "g": ["a"] * 150 + ["b"] * 150})
plt.figure(figsize=(6, 4))
show(histogram_axes(df, "x", 15, "density"))
plt.figure(figsize=(6, 4))
show(kde_axes(df, "x"))
plt.figure(figsize=(6, 4))
show(kde_by_group(df, "x", "g", ["a", "b"]))
plt.figure(figsize=(6, 4))
show(ecdf_axes(df, "x"))

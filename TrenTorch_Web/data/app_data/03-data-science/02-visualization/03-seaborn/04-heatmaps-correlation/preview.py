import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

rng = np.random.default_rng(3)
a = rng.normal(size=120)
df = pd.DataFrame({"a": a, "b": 2 * a + rng.normal(size=120) * 0.6, "c": rng.normal(size=120), "d": -a + rng.normal(size=120)})
corr = correlation_matrix(df)
print(corr.round(2))
plt.figure(figsize=(5, 4))
show(heatmap_axes(corr, True))
plt.figure(figsize=(5, 4))
show(masked_heatmap(corr))

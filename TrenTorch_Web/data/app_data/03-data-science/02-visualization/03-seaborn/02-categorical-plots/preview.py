import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

rng = np.random.default_rng(1)
df = pd.DataFrame({"team": rng.choice(["red", "blue", "green"], 90), "tier": rng.choice(["x", "y"], 90), "score": rng.normal(5, 2, 90)})
order = ranked_order(df, "team", "score")
print("teams, best first:", order)
plt.figure(figsize=(6, 4))
show(mean_bars(df, "team", "score", order))
plt.figure(figsize=(6, 4))
show(count_bars(df, "team", "tier", order, ["x", "y"]))
plt.figure(figsize=(6, 4))
show(horizontal_means(df, "team", "score", order))

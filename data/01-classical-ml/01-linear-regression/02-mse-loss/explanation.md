`np.mean(...)` returns `np.float64`, not a Python `float` — the `float(...)` wrapper isn't decoration, it's the actual fix for "must return a plain float."

`(y_hat - y) ** 2` computes every sample's squared error in one vectorized pass before the mean collapses it to a single number — no intermediate loop, no temporary list.

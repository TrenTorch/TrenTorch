import numpy as np

rng = np.random.default_rng(0)
x = rng.uniform(0, 10, 40)
y = 2 * x + rng.normal(0, 3, 40)
y[[5, 20]] += [15, -14]
fig, ax, points = scatter_chart(x, y, 20 + 5 * x, y, "value")
slope, intercept = fit_line(ax, x, y)
print(f"fit: y = {slope:.2f} x + {intercept:.2f}")
print("outliers beyond 2 standard deviations:", highlight_outliers(ax, x, y, 2.0))
show(fig)

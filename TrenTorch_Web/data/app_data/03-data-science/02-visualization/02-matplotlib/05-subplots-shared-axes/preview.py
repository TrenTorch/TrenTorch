import numpy as np

x = np.linspace(0, 6, 40)
series = {"sin": (x, np.sin(x)), "cos": (x, np.cos(x)), "damped": (x, np.exp(-x / 3) * np.sin(2 * x))}
fig, axes = small_multiples(series, 2)
show(fig)
fig2, left, right = twin_axis_chart(x, x**2, 100 / (1 + x), "revenue (EUR)", "conversion (%)")
show(fig2)

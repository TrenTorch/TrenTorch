import numpy as np

rng = np.random.default_rng(1)
a = rng.normal(0, 1, 300)
b = rng.normal(1.5, 1.2, 300)
fig, ax, counts, edges = draw_histogram(a, 12)
print("counts:", counts.astype(int).tolist())
show(fig)
show(density_histogram(a, 12)[0])
show(overlay_histograms(a, b, 15, ("control", "treated"))[0])

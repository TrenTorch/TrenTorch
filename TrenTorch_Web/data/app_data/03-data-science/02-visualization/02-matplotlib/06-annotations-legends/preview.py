import numpy as np
import matplotlib.pyplot as plt

x = np.arange(12)
y = np.array([3, 5, 4, 7, 9, 6, 5, 8, 12, 10, 7, 6.0])
fig, ax = plt.subplots()
ax.plot(x, y, label="signups")
annotate_max(ax, x, y)
add_threshold(ax, 8, "goal")
shade_region(ax, 3.5, 6.5, "campaign")
legend_below(ax, "Legend")
show(fig)

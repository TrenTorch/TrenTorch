labels = ["Q1", "Q2", "Q3"]
fig, ax = bar_chart(labels, [30, 45, 28])
print("labels:", annotate_bars(ax))
show(fig)
show(grouped_bars(labels, {"2023": [10, 20, 30], "2024": [12, 18, 35]})[0])
fig3, ax3 = stacked_bars(labels, {"web": [10, 20, 15], "store": [5, 8, 9], "app": [3, 4, 6]})
annotate_bars(ax3)
show(fig3)

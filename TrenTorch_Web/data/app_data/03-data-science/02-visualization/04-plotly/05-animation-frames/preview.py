import pandas as pd

df = pd.DataFrame(
    {
        "gdp": [1.0, 2.0, 3.0, 1.5, 2.5, 4.5, 2.0, 3.5, 6.0],
        "life": [50.0, 60.0, 70.0, 55.0, 62.0, 75.0, 58.0, 66.0, 80.0],
        "year": [2000, 2000, 2000, 2010, 2010, 2010, 2020, 2020, 2020],
    }
)
fig = animated_scatter(df, "gdp", "life", "year")
print("last frame:", last_frame_summary(fig))
show(fig)
show(figure_from_frames({"a": ([1, 2, 3], [4, 5, 6]), "b": ([2, 3, 4], [1, 1, 2]), "c": ([9, 8], [3, 3])}))

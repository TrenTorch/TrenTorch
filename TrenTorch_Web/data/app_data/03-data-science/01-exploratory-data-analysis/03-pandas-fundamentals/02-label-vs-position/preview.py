import pandas as pd

df = pd.DataFrame(
    {"city": ["Pune", "Delhi", "Goa", "Agra", "Kochi"], "temp": [31, 38, 29, 40, 30]},
    index=[10, 20, 30, 40, 50],
)
print(df)
print("\nrows_by_label(20, 40): both ends included")
print(rows_by_label(df, 20, 40))
print("\nrows_by_position(1, 3): the stop is excluded")
print(rows_by_position(df, 1, 3))
print("\ncell(30, 'city'):", cell(df, 30, "city"))
print("numeric_columns:", numeric_columns(df))
print("\nwith_value_where(temp > 35, 'city', 'HOT'):")
print(with_value_where(df, df["temp"] > 35, "city", "HOT"))

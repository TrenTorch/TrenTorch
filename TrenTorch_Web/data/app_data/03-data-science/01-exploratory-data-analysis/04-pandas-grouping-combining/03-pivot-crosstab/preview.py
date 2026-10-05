import pandas as pd

sales = pd.DataFrame(
    {
        "region": ["south", "north", "north", "south", "north", "east"],
        "quarter": ["Q2", "Q1", "Q1", "Q1", "Q3", "Q2"],
        "revenue": [10, 5, 7, 20, 3, 8],
    }
)
grid = revenue_pivot(sales)
print("revenue pivot:")
print(grid)
print("\nwith totals:")
print(add_totals(grid))
people = pd.DataFrame({"plan": ["b", "a", "b", "b"], "region": ["n", "n", "s", "n"]})
counts = count_table(people, "plan", "region")
print("\ncounts:")
print(counts)
print("\nrow percentages:")
print(row_percentages(counts))
wide = pd.DataFrame({"city": ["Pune", "Goa"], "jan": [1, 2], "feb": [4, 5]})
print("\nwide to long:")
print(to_long(wide, "city", "month", "sales"))

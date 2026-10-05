import pandas as pd

df = pd.DataFrame(
    {
        "name": ["Asha", "Ben", "Chen", "Dia", "Eli"],
        "city": ["Pune", "Delhi", "Pune", "Goa", "Delhi"],
        "age": [25, 41, 30, None, 52],
        "score": [7.5, 3.0, None, 9.0, 6.0],
    }
)
print(df)
print("\nin_range(age, 30, 50):")
print(in_range(df, "age", 30, 50))
print("\nPune or Delhi and age >= 30:")
print(from_cities_and_old_enough(df, ["Pune", "Delhi"], 30))
print("\nany_extreme(score, 4, 8):")
print(any_extreme(df, "score", 4, 8))
print("\nexclude_values(city, ['Pune']):")
print(exclude_values(df, "city", ["Pune"]))
print("\ncomplete_rows(['age', 'score']):")
print(complete_rows(df, ["age", "score"]))

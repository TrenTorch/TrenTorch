import pandas as pd

df = pd.DataFrame(
    {"dept": ["ops", "dev", "dev", "ops", "dev"], "salary": [50, 70, 70, 50, 90], "name": list("ABCDE")}
)
print("sort by dept, then salary descending:")
print(sort_by_columns(df, ["dept", "salary"], [True, False]))
scores = pd.Series([90, 80, 80, 70], index=list("wxyz"))
for method in ("min", "dense", "average"):
    print(f"\nrank ({method}):", rank_scores(scores, method).tolist())
print("\ntop 2 salaries:")
print(top_n(df, "salary", 2))
print("\npercent rank:", percent_rank(scores).round(2).tolist())

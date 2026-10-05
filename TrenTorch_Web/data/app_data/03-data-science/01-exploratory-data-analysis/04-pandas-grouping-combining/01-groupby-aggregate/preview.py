import pandas as pd

df = pd.DataFrame(
    {
        "dept": ["ops", "dev", "dev", "ops", "dev", "hr"],
        "salary": [50, 70, 90, 60, 80, None],
        "name": list("ABCDEF"),
    }
)
print("group_summary:")
print(group_summary(df, "dept", "salary"))
print("\nadd_group_mean:")
print(add_group_mean(df, "dept", "salary"))
print("\nz-score within group:")
print(zscore_within_group(df, "dept", "salary").round(2))
print("\ntop 2 per group:")
print(top_n_per_group(df, "dept", "salary", 2))

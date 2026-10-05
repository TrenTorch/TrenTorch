import pandas as pd

a = make_series([10, 20, 30], ["mon", "tue", "wed"], "sales")
b = make_series([1, 2, 3], ["tue", "wed", "thu"], "returns")
print("a + b, matched by label (a missing label gives NaN):")
print(aligned_sum(a, b))
print("\nwith fill_value=0:")
print(aligned_sum(a, b, fill_value=0))
print("\nshare of total:")
print(share_of_total(a))
print("\nlookup, with a label that does not exist:")
print(lookup(a, ["wed", "fri"]))

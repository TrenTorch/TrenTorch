import pprint
import pandas as pd

df = pd.DataFrame(
    {
        "age": [25, 30, 30, None, 41],
        "city": ["Pune", "Delhi", "Delhi", "Pune", None],
        "member": [True, False, True, True, False],
    }
)
print(df)
print()
pprint.pprint(profile(df), sort_dicts=False)

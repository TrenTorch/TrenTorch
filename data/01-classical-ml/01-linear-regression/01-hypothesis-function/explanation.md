`X @ w` relies on NumPy matmul treating a 1-D `(n_features,)` array on the right as a column vector, so it broadcasts against `(n_samples, n_features)` and produces `(n_samples,)` directly — no reshape needed. Adding scalar `b` broadcasts across every sample for free.

No dtype cast happens anywhere on purpose: whatever dtype `X` arrives in passes straight through, which is what "preserve dtype" in the requirements actually meant.

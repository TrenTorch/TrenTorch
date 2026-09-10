Computes `z = X @ w + b` and `p = sigmoid(z)` inline rather than through a separate `linear_forward` call — `sigmoid` needs the raw score `z` as an intermediate value it can reuse conceptually, and keeping both visible here makes the forward pass's two stages (linear score, then squash) explicit rather than hidden behind one function name.

Note on the `_load` import: dev-repo convenience so this file is independently runnable via `pytest`. In the actual student-facing Pyodide session, `sigmoid`/`bce_grad` are already defined in the same running session from earlier questions in this track.

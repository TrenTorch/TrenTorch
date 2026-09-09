`w = np.zeros(X.shape[1])`, not a hardcoded size — this is what lets the function work for any `n_features` without the caller passing it separately.

The loop body is `linear_forward` → `mse_grad` → `gd_step` in sequence and _nothing else_; no computation is reimplemented here, only wired together — every actual formula stays owned by the function that was already tested for it.

Note on the `_load` import at the top: that's a dev-repo convenience so this file is independently runnable via `pytest` outside the app. In the actual student-facing Pyodide session, `linear_forward`/`mse_grad`/`gd_step` are already defined in the same running session from the earlier questions in this track — a real student's version of this function calls them directly, no import needed.

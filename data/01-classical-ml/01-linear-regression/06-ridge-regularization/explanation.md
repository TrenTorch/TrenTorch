Calls `mse_grad(X, y_hat, y)` rather than reimplementing the base gradient inline — same "wire, don't reimplement" discipline as the training-loop question.

Only `dw` gets `+ 2 * lam * w`; `db` is returned untouched straight from `mse_grad`, which is what actually _enforces_ "bias is never regularized" rather than just asserting it in a comment.

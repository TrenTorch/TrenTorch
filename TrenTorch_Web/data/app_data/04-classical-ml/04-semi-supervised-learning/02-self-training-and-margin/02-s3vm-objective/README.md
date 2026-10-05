---
name: semi-supervised-s3vm-objective
title: 'Semi-supervised SVM objective with unlabeled hinge'
tags: [classical-ml, semi-supervised, svm, s3vm, hinge-loss, transductive]
difficulty: Advanced
---

## Statement

### Score the transductive SVM objective

A transductive SVM (Joachims, 1999) adds a penalty on unlabeled points that pushes them away from the decision boundary. For a linear score `f(x) = w^T x + b`, the objective is

`J = 0.5 ||w||^2 + C * sum_l max(0, 1 - y_l f(x_l)) + C_u * sum_u max(0, 1 - |f(x_u)|)`.

The unlabeled term is zero when a point lies at least margin 1 from the boundary, whichever side it is on, so it rewards separation and not a particular label.

Implement `s3vm_objective(w, b, X_l, y_l, X_u, C, C_u)` and return `J` as a float.

### Constraints

- `w` is 1-D. `X_l` is `(n_l, d)`, `y_l` holds values in `{-1, +1}`, and `X_u` is `(n_u, d)`.
- `C` and `C_u` must be nonnegative.
- Labels other than `-1` and `+1` raise `ValueError`.
- Shape mismatches raise `ValueError`.
- `X_u` may be empty, in which case its term is zero.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Use `np.maximum(0, 1 - y * f)` for the labeled hinge and `np.maximum(0, 1 - np.abs(f))` for the unlabeled one.

</details>

## Theory

The objective is non-convex because of the `|f|` term, so transductive SVM training is a hard optimization problem with many local minima. The symmetric hinge on unlabeled data is what makes it useful: it does not assume a label, only that a good boundary should pass through low-density regions. Setting `C_u` to zero recovers an ordinary SVM trained only on the labeled points.

### Where this shows up in production

Transductive SVMs are rarely deployed directly today because of their cost, but the idea of low-density separation lives on in cluster-assumption methods used for text and biomedical classification with few annotations. The practical value is as a diagnostic: if adding unlabeled data with `C_u > 0` makes the boundary cut through dense regions, the data violates the low-density assumption and a different method is warranted.

### Using it to make decisions

Use it when labels are scarce, the classes are roughly separated by a low-density gap, and a linear boundary is adequate. Tune `C` and `C_u` on a labeled validation split, and compare the final boundary against a plain SVM. Treat the objective as a diagnostic first: if the value drops sharply when unlabeled points are added, inspect where the boundary now lies relative to the unlabeled cloud.

### Pros and cons

**Pros:** uses unlabeled geometry directly, reduces to a standard SVM when `C_u = 0`, and gives an objective you can inspect and debug.

**Cons:** non-convex, so optimizers find different local solutions, scaling to large data is hard, and performance depends on the low-density assumption being true.

## Explanation

The function evaluates the regularizer and both hinge sums directly from the scores. Using `np.abs` on the unlabeled scores is the only change from a standard SVM hinge, and it is what lets unlabeled points push the boundary toward empty space.

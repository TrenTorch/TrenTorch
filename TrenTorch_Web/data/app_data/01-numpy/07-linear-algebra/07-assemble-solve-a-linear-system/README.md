---
name: numpy-assemble-solve-a-linear-system
title: 'Assemble: Solve a Small Linear System End to End'
tags: [numpy-core]
difficulty: Advanced
---

## Statement

Implement a single function that combines every topic in this module — matrix multiplication, transpose, norms, invertibility checking, and solving — into one realistic linear-system workflow, including verifying the solution with a norm-based error measure.

## Theory

This problem introduces no new concepts. It combines every topic covered in this module into one function, matching the "assemble" pattern used elsewhere on TrenTorch.

Specifically, this requires:

- Checking whether a system's coefficient matrix is invertible before attempting to solve it.
- Solving the system using the preferred method from this module.
- Verifying the solution by substituting it back into the original equation and measuring the resulting error with a norm.

Re-read the earlier topics in this module if a specific requirement below is unclear.

## Explanation

`is_solvable = abs(np.linalg.det(coefficients)) > 1e-10` checks invertibility directly. If not solvable, return immediately with `None` fields. Otherwise `solution = np.linalg.solve(coefficients, constants)`, `residual = coefficients @ solution - constants`, `residual_norm = np.linalg.norm(residual)` — a correctly solved system produces a residual vector very close to zero, so its norm is a single number near zero confirming the solve actually worked, rather than trusting the solver blindly.

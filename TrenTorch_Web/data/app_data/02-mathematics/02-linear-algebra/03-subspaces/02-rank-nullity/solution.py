import numpy as np

TOLERANCE = 1e-10


def rank(A):
    M = A.astype(float).copy()
    rows, cols = M.shape
    pivot_row = 0
    pivot_count = 0

    for col in range(cols):
        if pivot_row >= rows:
            break

        pivot = None
        for r in range(pivot_row, rows):
            if abs(M[r, col]) > TOLERANCE:
                pivot = r
                break
        if pivot is None:
            continue

        M[[pivot_row, pivot]] = M[[pivot, pivot_row]]

        for r in range(pivot_row + 1, rows):
            multiplier = M[r, col] / M[pivot_row, col]
            M[r] = M[r] - multiplier * M[pivot_row]

        pivot_row += 1
        pivot_count += 1

    return pivot_count


def nullity(A):
    return A.shape[1] - rank(A)

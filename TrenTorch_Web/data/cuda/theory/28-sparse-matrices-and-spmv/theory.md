# Sparse matrices and SpMV

## Why sparse

A matrix with mostly zeros (graphs, finite elements, pruned networks) wastes memory and time if stored densely. Store only the nonzeros plus their positions, and write kernels whose access patterns follow the data.

## Formats and their GPU personalities

Take the 4×4 matrix with rows `[5 0 0 1]`, `[0 2 0 0]`, `[0 0 0 0]`, `[3 0 4 6]`.
| Format | Stored | Strength | Weakness |
|---|---|---|---|
| **COO** (coordinate) | (row, col, val) per nonzero | simple, order-free | 12 B/nnz, needs atomics or segmented reduction |
| **CSR** (compressed sparse row) | `val[]`, `col[]`, `rowptr[]` | compact (≈ 8 B/nnz + 4 B/row), row access fast | rows have varying length ⇒ imbalance, divergence |
| **ELL** (ELLPACK) | each row padded to the max row length, stored **column-major** | perfectly regular, coalesced | padding waste when row lengths vary |
| **HYB / hybrid** | ELL for the regular part + COO for overflow | balances regularity and waste | more complex |
CSR here: `val=[5,1,2,3,4,6]`, `col=[0,3,1,0,2,3]`, `rowptr=[0,2,3,3,6]`. Row *r* occupies `val[rowptr[r] .. rowptr[r+1]−1]`.

## SpMV (y = A x) mappings

1. **One thread per row (CSR scalar):** simple; adjacent threads read `val` at addresses separated by their row lengths ⇒ **uncoalesced**, and a warp runs as long as its **longest** row (loop divergence, C1).
2. **One warp per row (CSR vector):** the 32 lanes stride across the row (coalesced loads of `val`, `col`), then warp-shuffle reduce (F1). Good for rows ≳ 32 nonzeros; wasteful for short rows (most lanes idle).
3. **ELL:** thread per row, column-major storage ⇒ at each step adjacent threads read adjacent addresses ⇒ perfectly coalesced.
4. **Merge-based / nonzero-split:** assign equal numbers of nonzeros to each thread block, then fix row boundaries with a co-rank-style search (E8); load-balanced for any row-length distribution.

## Arithmetic intensity and the roofline

Per nonzero: 2 FLOPs (multiply + add); bytes ≈ 4 (val) + 4 (col) + 4 (gather of `x[col]`, assuming cache misses) = **12 B ⇒ AI ≈ 0.17 FLOP/B**. On an A100 the roofline ceiling is 0.167 × 2,039 ≈ **340 GFLOP/s, 1.7% of the 19.5 TFLOPS peak**. SpMV is the canonical memory-bound, irregular kernel: only fewer bytes (better formats, caching `x`, smaller index types, reordering for locality) help. Gather accesses `x[col]` are uncoalesced; reordering rows/columns (e.g., reverse Cuthill-McKee) improves cache hits.

## Padding cost in ELL

Waste = (rows × max_len − nnz) / (rows × max_len). If 1,000 rows have lengths with mean 8 but one row has 500, ELL stores 500,000 slots for 8,492 nonzeros: **98% waste**, which is why HYB exists.

## Interactive: Same matrix, four layouts

<div class="cuda-viz" data-viz="VIZ-SPMV-FORMATS" data-title="Same matrix, four layouts" data-spec="VIZ-SPMV-FORMATS"></div>

## Check yourself

1. Write the CSR arrays for the matrix `[[0,2,0],[1,0,3],[0,0,0]]`.
2. Rows have 1-4 nonzeros. Better mapping: thread-per-row or warp-per-row? Why?
3. Why is SpMV stuck below 2% of peak FLOPs?

<details class="answers">
<summary>Show answers</summary>

1. val = [2,1,3], col = [1,0,2], rowptr = [0,1,3,3].
2. thread-per-row (rows too short for 32 lanes).
3. AI ≈ 0.17.

</details>

## Pitfalls

- Using `int` row pointers when nnz > 2³¹.
- Ignoring the output `y` writes and `rowptr` reads when counting bytes.

## Proposed problem

<div class="coming-soon"><div class="cs-head"><strong>CU-053 SpMV (CSR)</strong><span class="cs-badge">Coming soon</span></div><p>implement thread-per-row, then warp-per-row; report shows sectors per load and lane utilization.</p></div>

*PMPP reference:* Ch. 14 (sparse matrix computation: COO, CSR, ELL, hybrid, JDS and their SpMV kernels; control divergence and memory divergence trade-offs).

## Further reading

- Bell & Garland, "Implementing Sparse Matrix-Vector Multiplication on Throughput-Oriented Processors" (2009)

### Design
Each thread computes a small output micro-tile, e.g. `RM x RN`, rather than one output. It loads an A fragment reused across `RN` accumulators and a B fragment reused across `RM` accumulators:
```text
for each K tile:
    load RM A values and RN B values
    for r in 0..RM-1:
        for c in 0..RN-1:
            acc[r][c] += Afrag[r] * Bfrag[c]
```

### Why coarsen
More work per thread amortizes indexing and improves register reuse. But accumulator count grows as `RM*RN`; excessive coarsening increases register pressure, spills, and reduces occupancy. Select micro-tile dimensions based on register budget and shared-memory layout, then benchmark. This section describes the core mapping; the exact launch kernel should be specialized to the chosen tile and architecture.

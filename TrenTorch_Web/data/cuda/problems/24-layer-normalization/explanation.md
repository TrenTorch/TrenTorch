### Recommended strategy
Use a block-per-row reduction. Welford tuple reduction can obtain stable mean/variance in one read pass, then threads reread or retain values to write normalized outputs. A two-pass row algorithm is simpler: compute mean, then variance. The best strategy depends on row width, register capacity, and accuracy needs.

### Optimization
Fuse affine transformation into the normalization output. For long rows, avoid excessive per-thread registers and low occupancy. Match population-variance and epsilon semantics exactly.

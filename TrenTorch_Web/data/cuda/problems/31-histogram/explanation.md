### Baseline
```cpp
__global__ void histogram_global(const int* x, unsigned* hist,
                                 int n, int bins) {
    int i=blockIdx.x*blockDim.x+threadIdx.x;
    if (i<n) {
        int b=x[i];
        if (b>=0 && b<bins) atomicAdd(&hist[b], 1u);
    }
}
```
Initialize `hist` to zero before launch.

### Privatized approach
Each block creates a shared histogram, initializes it, atomically increments local bins, synchronizes, then merges nonzero/local counts to global memory. This reduces global atomic contention but uses shared memory and still needs global merging. For very large bin counts, shared-memory capacity may prohibit full privatization.

### Performance considerations
Uniform random keys, highly skewed keys, and small bin counts behave differently. Warp-aggregated atomics, multiple sub-histograms per block, and partial-histogram reduction are alternatives. Include initialization and merge costs in benchmarks.

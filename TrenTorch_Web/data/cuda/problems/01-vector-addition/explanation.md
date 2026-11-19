### Baseline and recommended kernel
```cpp
__global__ void vector_add(const float* A, const float* B,
                           float* C, int N) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < N) C[i] = A[i] + B[i];
}
```
Launch with `threads = 256` (a starting point) and `blocks = (N + threads - 1) / threads`.

### Why this design
Each thread performs one addition and accesses three contiguous arrays. Adjacent lanes access adjacent 4-byte words, producing coalesced global-memory transactions. The kernel transfers at least `4N + 4N + 4N = 12N` bytes (two reads and one write) and performs `N` additions, so arithmetic intensity is `1/12` FLOP/byte if an addition counts as one FLOP. It is normally bandwidth-bound for large `N`; for small `N`, launch and dispatch overhead dominate.

### Optimization and validation
- Fuse vector addition into a neighboring operation when possible to eliminate an intermediate read/write.
- A grid-stride loop can cap grid size and support very large arrays.
- Try 128, 256, and 512 threads per block; do not assume the largest block wins.
- Validate `N=0`, `N=1`, non-multiples of block size, and large `N`.

**Complexity:** `O(N)` work, `O(N)` memory traffic, `O(1)` extra storage.

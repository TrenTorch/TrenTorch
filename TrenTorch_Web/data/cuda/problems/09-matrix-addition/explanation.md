### Kernel
```cpp
__global__ void matrix_add(const float* A, const float* B,
                           float* C, int H, int W) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;
    if (x < W && y < H) {
        int i = y * W + x;
        C[i] = A[i] + B[i];
    }
}
```
A common starting block is `(32, 8)` or `(32, 4)`, so a warp spans the contiguous x dimension.

### Analysis
The x coordinate maps to adjacent columns and adjacent addresses. Mapping y to the fastest lane dimension would create strided accesses and poor coalescing. Total traffic is `12HW` bytes.

### Naive kernel
```cpp
__global__ void matmul_naive(const float* A, const float* B, float* C,
                             int M, int N, int K) {
    int col=blockIdx.x*blockDim.x+threadIdx.x;
    int row=blockIdx.y*blockDim.y+threadIdx.y;
    if (row<M && col<N) {
        float acc=0.f;
        for (int k=0;k<K;++k)
            acc=fmaf(A[(size_t)row*K+k], B[(size_t)k*N+col], acc);
        C[(size_t)row*N+col]=acc;
    }
}
```

### Analysis
Each output performs `K` multiply-adds. Without reuse, the conceptual load count is roughly `2K` input values per output, although caches may reduce actual DRAM traffic. This is a poor arithmetic-intensity design compared with tiled matmul.

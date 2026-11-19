### Kernel (square tile `T`)
```cpp
template<int T>
__global__ void matmul_tiled(const float* A, const float* B, float* C,
                             int M, int N, int K) {
    __shared__ float As[T][T];
    __shared__ float Bs[T][T];
    int row=blockIdx.y*T+threadIdx.y;
    int col=blockIdx.x*T+threadIdx.x;
    float acc=0.f;
    for (int tile=0; tile<(K+T-1)/T; ++tile) {
        int ak=tile*T+threadIdx.x;
        int bk=tile*T+threadIdx.y;
        As[threadIdx.y][threadIdx.x] =
            (row<M && ak<K) ? A[(size_t)row*K+ak] : 0.f;
        Bs[threadIdx.y][threadIdx.x] =
            (bk<K && col<N) ? B[(size_t)bk*N+col] : 0.f;
        __syncthreads();
        #pragma unroll
        for (int k=0;k<T;++k) acc=fmaf(As[threadIdx.y][k],
                                        Bs[k][threadIdx.x],acc);
        __syncthreads();
    }
    if (row<M && col<N) C[(size_t)row*N+col]=acc;
}
```

### Why it improves reuse
A tile of `T x T` outputs reuses each loaded A/B tile value across multiple multiply-adds. The two barriers ensure tiles are fully loaded before use and not overwritten before all threads finish consuming them. Edge tiles load zeros for out-of-range coordinates.

### Tuning
Try tile sizes compatible with hardware resources and warp mapping. Larger tiles improve reuse but increase shared-memory/register use and can lower occupancy. For high performance on modern GPUs, use optimized library kernels/Tensor Cores when allowed; this simple kernel is an educational baseline.

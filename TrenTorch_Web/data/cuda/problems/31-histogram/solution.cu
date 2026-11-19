__global__ void histogram(const int* x, unsigned* hist, int n, int bins) {
    __shared__ unsigned local[64];                 // private copy for this block
    for (int b = threadIdx.x; b < bins; b += blockDim.x) local[b] = 0;
    __syncthreads();

    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) {
        int b = x[i];
        if (b >= 0 && b < bins) atomicAdd(&local[b], 1);
    }
    __syncthreads();

    for (int b = threadIdx.x; b < bins; b += blockDim.x) {
        if (local[b] > 0) atomicAdd(&hist[b], local[b]);
    }
}

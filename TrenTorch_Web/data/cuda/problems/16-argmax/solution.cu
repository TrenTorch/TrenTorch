__global__ void argmax_partials(const float* X, float* pval, int* pidx, int N) {
    __shared__ float sval[256];
    __shared__ int sidx[256];
    int t = threadIdx.x;
    int i = blockIdx.x * blockDim.x + t;
    sval[t] = (i < N) ? X[i] : -INFINITY;
    sidx[t] = (i < N) ? i : INT_MAX;
    __syncthreads();
    for (int d = blockDim.x / 2; d > 0; d >>= 1) {
        if (t < d) {
            float bv = sval[t + d];
            int bi = sidx[t + d];
            if (bv > sval[t] || (bv == sval[t] && bi < sidx[t])) {
                sval[t] = bv;
                sidx[t] = bi;
            }
        }
        __syncthreads();
    }
    if (t == 0) {
        pval[blockIdx.x] = sval[0];
        pidx[blockIdx.x] = sidx[0];
    }
}

__global__ void argmax_final(const float* pval, const int* pidx, int* out, int blocks) {
    __shared__ float sval[256];
    __shared__ int sidx[256];
    int t = threadIdx.x;
    sval[t] = (t < blocks) ? pval[t] : -INFINITY;
    sidx[t] = (t < blocks) ? pidx[t] : INT_MAX;
    __syncthreads();
    for (int d = blockDim.x / 2; d > 0; d >>= 1) {
        if (t < d) {
            float bv = sval[t + d];
            int bi = sidx[t + d];
            if (bv > sval[t] || (bv == sval[t] && bi < sidx[t])) {
                sval[t] = bv;
                sidx[t] = bi;
            }
        }
        __syncthreads();
    }
    if (t == 0) out[0] = sidx[0];
}

__global__ void argmax_partials(const float* X, float* pval, int* pidx, int N) {
    __shared__ float sval[256];
    __shared__ int sidx[256];
    // TODO: each thread starts from (X[i], i) or (-INFINITY, INT_MAX); keep the better pair at every step.
}

__global__ void argmax_final(const float* pval, const int* pidx, int* out, int blocks) {
    __shared__ float sval[256];
    __shared__ int sidx[256];
    // TODO: out[0] = the winning index.
}

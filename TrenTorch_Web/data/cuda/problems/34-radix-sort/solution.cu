__global__ void radix_pass(const int* in, int* out, int n, int bit) {
    __shared__ int scan[1024];
    int t = threadIdx.x;
    int key = (t < n) ? in[t] : 0;
    int isZero = (t < n && ((key >> bit) & 1) == 0) ? 1 : 0;

    // inclusive Hillis-Steele scan of the zero flags
    scan[t] = isZero;
    __syncthreads();
    for (int off = 1; off < blockDim.x; off <<= 1) {
        int v = (t >= off) ? scan[t - off] : 0;
        __syncthreads();
        scan[t] += v;
        __syncthreads();
    }
    int zerosBefore = scan[t] - isZero;       // exclusive scan
    int zerosTotal = scan[blockDim.x - 1];

    if (t < n) {
        int dst = isZero ? zerosBefore : zerosTotal + (t - zerosBefore);
        out[dst] = key;
    }
}

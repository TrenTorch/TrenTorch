__global__ void radix_pass(const int* in, int* out, int n, int bit) {
    __shared__ int flags[1024];
    int t = threadIdx.x;
    // TODO: flags[t] = 1 when key t has bit == 0; exclusive-scan the flags in shared memory; scatter to out.
}

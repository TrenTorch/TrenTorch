__global__ void warp_sum_kernel(const float* X, float* out, int N) {
    // TODO: v = this lane's element (or 0), then a shuffle-down loop with offsets 16, 8, 4, 2, 1.
}

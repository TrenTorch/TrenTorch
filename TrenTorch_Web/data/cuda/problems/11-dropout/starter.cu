__global__ void dropout_hash(const float* X, float* Y, int N, float keep_prob, unsigned seed) {
    // TODO: hash (i, seed) into a uniform u in [0, 1), then keep when u < keep_prob.
}

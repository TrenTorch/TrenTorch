__global__ void saxpy_any_block(float a, const float* x, float* y, int n) {
    // TODO: grid-stride loop so every element is covered regardless of the launch shape.
}

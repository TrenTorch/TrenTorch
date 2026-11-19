#include <cuda_runtime.h>
#include <nccl.h>
#include <cstdio>

int main() {
    const int n = 4;        // GPUs
    const int count = 8;    // floats per GPU
    ncclComm_t comms[4];
    ncclCommInitAll(comms, n);

    float *d_send[4];
    float *d_recv[4];
    float h_val[8];
    for (int r = 0; r < n; r++) {
        for (int i = 0; i < count; i++) h_val[i] = (r == 0) ? 7.5f : 0.0f;   // only rank 0 has data
        cudaSetDevice(r);
        cudaMalloc(&d_send[r], count * sizeof(float));
        cudaMalloc(&d_recv[r], count * sizeof(float));
        cudaMemcpy(d_send[r], h_val, count * sizeof(float), cudaMemcpyHostToDevice);
    }

    // TODO: broadcast rank 0's d_send into d_recv on every GPU.

    float h_out[8];
    for (int r = 0; r < n; r++) {
        cudaSetDevice(r);
        cudaMemcpy(h_out, d_recv[r], count * sizeof(float), cudaMemcpyDeviceToHost);
        printf("rank %d: %f\n", r, h_out[0]);
    }
    return 0;
}

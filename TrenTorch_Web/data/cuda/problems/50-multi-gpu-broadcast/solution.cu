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

    // every rank makes the same call; rank 0 is the root
    for (int r = 0; r < n; r++) {
        cudaSetDevice(r);
        ncclBroadcast(d_send[r], d_recv[r], count, ncclFloat, 0, comms[r], 0);
    }

    float h_out[8];
    for (int r = 0; r < n; r++) {
        cudaSetDevice(r);
        cudaMemcpy(h_out, d_recv[r], count * sizeof(float), cudaMemcpyDeviceToHost);
        printf("rank %d: %f\n", r, h_out[0]);
    }
    return 0;
}

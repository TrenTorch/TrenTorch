### Typical bug
Threads cooperatively write a shared tile and some threads read it before all producers have completed.

### Fix
Place `__syncthreads()` after cooperative loading and before any thread reads values produced by other threads. If the shared buffer is reused in a loop, add a second barrier after consumers finish and before the next iteration overwrites the tile.

### Diagnostic process
1. Identify every shared-memory producer and consumer.
2. Draw the required happens-before edges.
3. Check that all threads in the block reach each block barrier.
4. Run Compute Sanitizer (`compute-sanitizer --tool racecheck`) where supported.
5. Test partial tiles and boundary paths, which often contain divergent control flow.

# Barriers and divergent barriers

## What `__syncthreads()` guarantees

It is a **block-wide barrier**: no thread continues past it until every thread of the block has reached it, and all shared-memory writes made before it are visible to the whole block after it. It is the tool for turning "each thread wrote its piece" into "everyone can read all pieces".

```cuda
tile[t] = global_data[i];   // each thread writes one slot
__syncthreads();            // wait until all slots are written
use(tile[(t + 1) % B]);     // now reading a neighbour's slot is safe
```

## The race it prevents

Without the barrier thread *t* may read slot *t+1* before thread *t+1* has written it. Three hazard names:
- **RAW** (read-after-write): read too early.
- **WAR** (write-after-read): overwrite a slot someone has not read yet. This is why tiled loops have a *second* barrier before loading the next tile.
- **WAW** (write-after-write): two threads write one slot with no order.

## The divergent barrier bug

Every thread of the block must reach the same `__syncthreads()`. If it sits inside an `if` that only some threads enter, the others never arrive. The behaviour is undefined: on hardware it can hang the kernel; in the simulator it is reported as a divergent-barrier diagnostic.

```cuda
if (idx < n) {            // BUG: threads with idx >= n skip the barrier
    tile[t] = in[idx];
    __syncthreads();
}
```
The fix is structural: keep *all* threads alive, **guard the loads and stores, not the barrier**.
```cuda
tile[t] = (idx < n) ? in[idx] : 0.0f;   // every thread participates
__syncthreads();
```
An early `return` for out-of-range threads before a barrier is the same bug in disguise.

## Interactive: Who is waiting at the fence?

<div class="cuda-viz" data-viz="VIZ-BARRIER-EPOCHS" data-title="Who is waiting at the fence?" data-spec="VIZ-BARRIER-EPOCHS"></div>

## Check yourself

1. Why does the tiled matmul loop need a barrier both after loading *and* before loading the next tile?
2. Can `__syncthreads()` synchronize two different blocks?
3. Rewrite the buggy snippet above so out-of-range threads still reach the barrier.

<details class="answers">
<summary>Show answers</summary>

1. first: RAW (tiles loaded), second: WAR (before overwriting).
2. No.
3. `tile[t] = (idx < n) ? in[idx] : 0; __syncthreads();`

</details>

## Practice

[CU-048 Bug Hunt: Shared-Memory Race](problem:CU-048) · [CU-050 Bug Hunt: Divergent Barrier](problem:CU-050)

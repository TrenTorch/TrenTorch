<!-- chapters: C2 -->
## 🎬 VIZ-BARRIER-EPOCHS: "Who is waiting at the fence?"
- *Canvas:* a timeline with one horizontal track per thread (8 shown), time on x. Vertical dashed lines mark `__syncthreads()` barriers dividing time into **epochs**. Above: a strip of 8 shared-memory slots.
- *Controls:* a code panel with checkboxes to **remove barrier #1**, **remove barrier #2**, and a toggle **Put the barrier inside `if (t < 4)`**; `Stepper`; **Speed** randomization toggle (threads progress at different speeds).
- *Animation:* threads advance at different speeds. At a barrier, the early ones stop and show a "waiting" hatch; when the slowest arrives, all release together. When barrier #1 is removed, a read arrow from thread 3 hits slot 4 before thread 4's write arrives: the slot flashes red "RAW race: read before write" with the thread ids. With the barrier in `if (t < 4)`, threads 4-7 never arrive; the four waiting tracks stay hatched and a banner says "DEADLOCK: 4 threads never reached the barrier".
- *Aha moment:* races depend on timing, so they can pass 99 runs and fail on the 100th; the viz forces the bad schedule so you see it.

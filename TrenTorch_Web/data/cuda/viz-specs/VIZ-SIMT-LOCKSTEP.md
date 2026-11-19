<!-- chapters: A2 -->
## 🎬 VIZ-SIMT-LOCKSTEP: "One instruction, thirty-two lanes"
- *Canvas:* a column of pseudo-assembly lines on the left (`LD r1, [in+i]`, `MAX r2, r1, 0`, `ST [out+i], r2`) with a pointer arrow; right, a `LaneStrip` of 32 lanes, each lane showing its own register values for `r1`, `r2` and its own `i`.
- *Controls:* `Stepper`. A data pattern dropdown: *all positive*, *alternating*, *random*.
- *Animation:* the pointer moves down one instruction per step; on each step all 32 lanes flash together and their register cells update with different values.
- *Aha moment:* same instruction, different data per lane. No lane is ahead of the others.
- *Accessibility:* "Instruction 2 of 3: MAX executed by 32 of 32 lanes."

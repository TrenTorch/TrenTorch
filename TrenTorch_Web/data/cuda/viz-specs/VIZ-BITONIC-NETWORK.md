<!-- chapters: E8 -->
## 🎬 VIZ-BITONIC-NETWORK: "A sort that never looks at the data"
- *Canvas:* a classic network diagram: 8 or 16 horizontal wires; vertical connectors are compare-exchange elements, arranged in stages. Arrows on each connector show the direction smaller values move.
- *Controls:* **N** (8 or 16), **Input** (editable), `Stepper`, toggle **Show stage number**.
- *Animation:* values travel along the wires; at each connector the pair swaps if out of order (the swap flashes). Stage counter ticks.
- *Readouts:* **stage**, **comparators executed**, **swaps made**.
- *Aha moment:* the wiring is identical for every input.

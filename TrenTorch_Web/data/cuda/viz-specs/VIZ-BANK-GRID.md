<!-- chapters: D5 -->
## 🎬 VIZ-BANK-GRID: "32 lanes, 32 banks"
- *Canvas:* left: a shared-memory array drawn as a matrix (rows × columns) with every cell labelled by its bank number (0-31) and tinted by bank. Right: 32 bank columns (vertical bars) and 32 lane squares along the top, with lines from each lane to its bank.
- *Controls:* **Access pattern** (row, column, stride *s*, broadcast), **Row padding** (0 or 1), **Tile width** (32), `Stepper`.
- *Animation:* press **Issue access**: lane lines fly to banks; banks with more than one request stack the requests vertically and turn red with a number "×k". The timeline underneath shows k sequential cycles instead of 1.
- *Readouts:* **max conflict degree**, **cycles**, **slowdown ×**.
- *Aha moment:* with the column pattern, toggle padding 0 → 1 and the 32-high red stack on one bank dissolves into a flat row of single requests; the bank labels in the matrix visibly shift per row.
- *Accessibility:* "Column access, no padding: all 32 lanes hit bank 5: 32-way conflict, 32 cycles."

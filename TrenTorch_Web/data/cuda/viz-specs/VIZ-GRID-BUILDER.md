<!-- chapters: B1 -->
## 🎬 VIZ-GRID-BUILDER: "Covering a matrix"
- *Canvas:* a matrix drawn as a grid of cells (up to 24×24 shown). Block tiles overlay it in alternating translucent colours, with block borders drawn thicker.
- *Controls:* **Matrix rows/cols**, **block shape** (drag the corner of a block, or choose 8×8, 16×16, 32×8, 32×32); toggle **x → col, y → row** versus **swapped**.
- *Animation:* hover a cell: its owning block and thread are highlighted, with the formulas for `row`, `col`, and `row*W+col` shown. Matrices that do not divide evenly show hatched out-of-range thread cells at the right and bottom edges.
- *Aha moment:* the swapped mapping is visibly legal but later (D1) shown to be slow.

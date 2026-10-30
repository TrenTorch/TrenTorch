// O(9^k) time (backtracking with MRV), O(81) space
function sudokuSolver(board) {
  const grid = board.map(row => row.slice());
  const rows = Array.from({ length: 9 }, () => new Set());
  const cols = Array.from({ length: 9 }, () => new Set());
  const boxes = Array.from({ length: 9 }, () => new Set());
  const empty = [];

  for (let r = 0; r < 9; r++) {
    for (let c = 0; c < 9; c++) {
      const v = grid[r][c];
      if (v !== 0) {
        rows[r].add(v);
        cols[c].add(v);
        boxes[Math.floor(r / 3) * 3 + Math.floor(c / 3)].add(v);
      } else {
        empty.push([r, c]);
      }
    }
  }

  function candidates(r, c) {
    const usedRow = rows[r];
    const usedCol = cols[c];
    const usedBox = boxes[Math.floor(r / 3) * 3 + Math.floor(c / 3)];
    const opts = [];
    for (let d = 1; d <= 9; d++) {
      if (!usedRow.has(d) && !usedCol.has(d) && !usedBox.has(d)) {
        opts.push(d);
      }
    }
    return opts;
  }

  function solve() {
    let best = null;
    let bestOpts = null;

    for (const [r, c] of empty) {
      if (grid[r][c] === 0) {
        const opts = candidates(r, c);
        if (best === null || opts.length < bestOpts.length) {
          best = [r, c];
          bestOpts = opts;
          if (opts.length <= 1) break;
        }
      }
    }

    if (best === null) return true; // solved

    const [r, c] = best;
    for (const v of bestOpts) {
      grid[r][c] = v;
      rows[r].add(v);
      cols[c].add(v);
      boxes[Math.floor(r / 3) * 3 + Math.floor(c / 3)].add(v);

      if (solve()) return true;

      grid[r][c] = 0;
      rows[r].delete(v);
      cols[c].delete(v);
      boxes[Math.floor(r / 3) * 3 + Math.floor(c / 3)].delete(v);
    }
    return false;
  }

  solve();
  return grid;
}

console.log(sudokuSolver([[5, 3, 0, 0, 7, 0, 0, 0, 0], [6, 0, 0, 1, 9, 5, 0, 0, 0], [0, 9, 8, 0, 0, 0, 0, 6, 0], [8, 0, 0, 0, 6, 0, 0, 0, 3], [4, 0, 0, 8, 0, 3, 0, 0, 1], [7, 0, 0, 0, 2, 0, 0, 0, 6], [0, 6, 0, 0, 0, 0, 2, 8, 0], [0, 0, 0, 4, 1, 9, 0, 0, 5], [0, 0, 0, 0, 8, 0, 0, 7, 9]]));

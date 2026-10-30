function largestIsland(grid) {
  // O(rows * cols) time, O(rows * cols) space
  const rows = grid.length;
  const cols = rows > 0 ? grid[0].length : 0;
  const label = Array.from({ length: rows }, () => Array(cols).fill(0));
  const size = new Map();
  let nextId = 1;

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (grid[r][c] === 1 && label[r][c] === 0) {
        label[r][c] = nextId;
        const stack = [[r, c]];
        let count = 0;
        while (stack.length) {
          const [x, y] = stack.pop();
          count++;
          const neighbors = [
            [x + 1, y],
            [x - 1, y],
            [x, y + 1],
            [x, y - 1]
          ];
          for (const [nx, ny] of neighbors) {
            if (
              nx >= 0 && nx < rows &&
              ny >= 0 && ny < cols &&
              grid[nx][ny] === 1 &&
              label[nx][ny] === 0
            ) {
              label[nx][ny] = nextId;
              stack.push([nx, ny]);
            }
          }
        }
        size.set(nextId, count);
        nextId++;
      }
    }
  }

  let best = 0;
  for (const v of size.values()) {
    if (v > best) best = v;
  }

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (grid[r][c] === 0) {
        const around = new Set();
        const neighbors = [
          [r + 1, c],
          [r - 1, c],
          [r, c + 1],
          [r, c - 1]
        ];
        for (const [nx, ny] of neighbors) {
          if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && label[nx][ny] !== 0) {
            around.add(label[nx][ny]);
          }
        }
        let sum = 1;
        for (const id of around) {
          sum += size.get(id);
        }
        if (sum > best) best = sum;
      }
    }
  }

  return best;
}

console.log(largestIsland([[1, 0], [0, 1]]));

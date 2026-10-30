// O(rows * cols) time, O(rows * cols) space
function shortestPathBinaryMatrix(grid) {
  const rows = grid.length;
  const cols = rows ? grid[0].length : 0;
  if (rows === 0 || cols === 0 || grid[0][0] === 1 || grid[rows - 1][cols - 1] === 1) {
    return -1;
  }
  const seen = Array.from({ length: rows }, () => Array(cols).fill(false));
  const queue = [];
  let head = 0;
  queue.push([0, 0, 1]);
  seen[0][0] = true;
  const dirs = [-1, 0, 1];
  while (head < queue.length) {
    const [x, y, steps] = queue[head++];
    if (x === rows - 1 && y === cols - 1) {
      return steps;
    }
    for (let dx of dirs) {
      for (let dy of dirs) {
        const nx = x + dx;
        const ny = y + dy;
        if (
          nx < 0 ||
          nx >= rows ||
          ny < 0 ||
          ny >= cols ||
          grid[nx][ny] !== 0 ||
          seen[nx][ny]
        ) {
          continue;
        }
        seen[nx][ny] = true;
        queue.push([nx, ny, steps + 1]);
      }
    }
  }
  return -1;
}

console.log(shortestPathBinaryMatrix([[0, 0, 0], [1, 1, 0], [1, 1, 0]]));

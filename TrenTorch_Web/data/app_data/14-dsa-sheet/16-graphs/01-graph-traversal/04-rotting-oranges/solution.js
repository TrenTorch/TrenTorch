// O(m * n) time, O(m * n) space where m = rows, n = cols
function orangesRotting(grid) {
  const rows = grid.length;
  const cols = rows > 0 ? grid[0].length : 0;
  
  // Deep copy grid
  const g = grid.map(row => [...row]);
  
  const queue = [];
  let fresh = 0;
  
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (g[r][c] === 2) {
        queue.push([r, c]);
      } else if (g[r][c] === 1) {
        fresh++;
      }
    }
  }
  
  let minutes = 0;
  const directions = [[1, 0], [-1, 0], [0, 1], [0, -1]];
  
  // Use index pointer for O(1) dequeue
  let qIndex = 0;
  
  while (qIndex < queue.length && fresh > 0) {
    minutes++;
    const levelSize = queue.length - qIndex;
    for (let i = 0; i < levelSize; i++) {
      const [x, y] = queue[qIndex++];
      for (const [dx, dy] of directions) {
        const nx = x + dx;
        const ny = y + dy;
        if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && g[nx][ny] === 1) {
          g[nx][ny] = 2;
          fresh--;
          queue.push([nx, ny]);
        }
      }
    }
  }
  
  return fresh === 0 ? minutes : -1;
}

console.log(orangesRotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]));

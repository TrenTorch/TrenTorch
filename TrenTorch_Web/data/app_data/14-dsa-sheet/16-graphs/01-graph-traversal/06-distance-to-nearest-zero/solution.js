// O(rows*cols) time, O(rows*cols) space
function nearestZero(mat) {
  const rows = mat.length;
  const cols = rows ? mat[0].length : 0;
  const dist = Array.from({ length: rows }, () => Array(cols).fill(-1));
  const queue = [];
  let qStart = 0;

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (mat[r][c] === 0) {
        dist[r][c] = 0;
        queue.push([r, c]);
      }
    }
  }

  const dirs = [
    [1, 0],
    [-1, 0],
    [0, 1],
    [0, -1],
  ];

  while (qStart < queue.length) {
    const [x, y] = queue[qStart++];
    const d = dist[x][y];
    for (const [dx, dy] of dirs) {
      const nx = x + dx;
      const ny = y + dy;
      if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && dist[nx][ny] === -1) {
        dist[nx][ny] = d + 1;
        queue.push([nx, ny]);
      }
    }
  }

  return dist;
}

console.log(nearestZero([[0, 0, 0], [0, 1, 0], [1, 1, 1]]));

// O(4^(rows*cols)) time, O(rows*cols) space
function ratInAMaze(maze) {
  const rows = maze.length;
  const cols = rows ? maze[0].length : 0;
  if (rows === 0 || cols === 0 || maze[0][0] === 0 || maze[rows - 1][cols - 1] === 0) {
    return [];
  }
  const out = [];
  const path = [];
  const onPath = Array.from({ length: rows }, () => Array(cols).fill(false));
  const moves = [
    ['D', 1, 0],
    ['L', 0, -1],
    ['R', 0, 1],
    ['U', -1, 0],
  ];

  function go(r, c) {
    if (r === rows - 1 && c === cols - 1) {
      out.push(path.join(''));
      return;
    }
    onPath[r][c] = true;
    for (const [letter, dr, dc] of moves) {
      const nr = r + dr;
      const nc = c + dc;
      if (
        nr >= 0 && nr < rows &&
        nc >= 0 && nc < cols &&
        maze[nr][nc] === 1 &&
        !onPath[nr][nc]
      ) {
        path.push(letter);
        go(nr, nc);
        path.pop();
      }
    }
    onPath[r][c] = false;
  }

  go(0, 0);
  return out;
}

console.log(ratInAMaze([[1, 0, 0, 0], [1, 1, 0, 1], [1, 1, 0, 0], [0, 1, 1, 1]]));

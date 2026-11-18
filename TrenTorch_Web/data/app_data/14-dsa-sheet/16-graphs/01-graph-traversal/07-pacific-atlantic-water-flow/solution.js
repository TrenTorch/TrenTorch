// O(m*n) time, O(m*n) space
function pacificAtlantic(heights) {
  const rows = heights.length;
  const cols = rows > 0 ? heights[0].length : 0;

  const flood = (starts) => {
    const seen = new Set();
    const stack = [];
    for (const [r, c] of starts) {
      const key = `${r},${c}`;
      seen.add(key);
      stack.push([r, c]);
    }
    while (stack.length > 0) {
      const [x, y] = stack.pop();
      const currentHeight = heights[x][y];
      const neighbors = [
        [x + 1, y],
        [x - 1, y],
        [x, y + 1],
        [x, y - 1]
      ];
      for (const [nx, ny] of neighbors) {
        if (nx >= 0 && nx < rows && ny >= 0 && ny < cols) {
          const nkey = `${nx},${ny}`;
          if (!seen.has(nkey) && heights[nx][ny] >= currentHeight) {
            seen.add(nkey);
            stack.push([nx, ny]);
          }
        }
      }
    }
    return seen;
  };

  const pacificStarts = [];
  for (let r = 0; r < rows; r++) pacificStarts.push([r, 0]);
  for (let c = 0; c < cols; c++) pacificStarts.push([0, c]);
  const pacific = flood(pacificStarts);

  const atlanticStarts = [];
  for (let r = 0; r < rows; r++) atlanticStarts.push([r, cols - 1]);
  for (let c = 0; c < cols; c++) atlanticStarts.push([rows - 1, c]);
  const atlantic = flood(atlanticStarts);

  const result = [];
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const key = `${r},${c}`;
      if (pacific.has(key) && atlantic.has(key)) {
        result.push([r, c]);
      }
    }
  }
  return result;
}

console.log(pacificAtlantic([[1, 2], [2, 1]]));

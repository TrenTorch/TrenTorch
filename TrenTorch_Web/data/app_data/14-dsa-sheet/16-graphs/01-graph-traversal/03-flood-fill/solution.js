// O(m*n) time, O(m*n) space where m=rows, n=cols
function floodFill(image, sr, sc, color) {
  const old = image[sr][sc];
  if (old === color) {
    return image;
  }
  const rows = image.length;
  const cols = image[0].length;
  image[sr][sc] = color;
  const stack = [[sr, sc]];
  while (stack.length > 0) {
    const [x, y] = stack.pop();
    const neighbors = [
      [x + 1, y],
      [x - 1, y],
      [x, y + 1],
      [x, y - 1]
    ];
    for (const [nx, ny] of neighbors) {
      if (nx >= 0 && nx < rows && ny >= 0 && ny < cols && image[nx][ny] === old) {
        image[nx][ny] = color;
        stack.push([nx, ny]);
      }
    }
  }
  return image;
}

console.log(floodFill([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2));

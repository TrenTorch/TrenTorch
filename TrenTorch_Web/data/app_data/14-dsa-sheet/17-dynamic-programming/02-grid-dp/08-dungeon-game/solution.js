// O(m*n) time, O(n) space
function calculateMinimumHp(dungeon) {
  const rows = dungeon.length;
  const cols = rows ? dungeon[0].length : 0;
  if (rows === 0 || cols === 0) {
    return 1;
  }
  const inf = Infinity;
  const need = new Array(cols + 1).fill(inf);
  need[cols - 1] = 1;
  for (let r = rows - 1; r >= 0; r--) {
    for (let c = cols - 1; c >= 0; c--) {
      let bestNext = Math.min(need[c], need[c + 1]);
      if (r === rows - 1 && c === cols - 1) {
        bestNext = 1;
      }
      need[c] = Math.max(1, bestNext - dungeon[r][c]);
    }
    need[cols] = inf;
  }
  return need[0];
}

console.log(calculateMinimumHp([[-2, -3, 3], [-5, -10, 1], [10, 30, -5]]));

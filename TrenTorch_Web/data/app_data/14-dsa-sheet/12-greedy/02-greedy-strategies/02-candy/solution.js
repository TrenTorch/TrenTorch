// O(n) time, O(1) space
function candy(ratings) {
  const n = ratings.length;
  if (n === 0) return 0;
  let total = 1;
  let up = 0, down = 0, peak = 0;
  for (let i = 1; i < n; i++) {
    if (ratings[i] > ratings[i - 1]) {
      up += 1;
      down = 0;
      peak = up;
      total += 1 + up;
    } else if (ratings[i] === ratings[i - 1]) {
      up = down = peak = 0;
      total += 1;
    } else {
      up = 0;
      down += 1;
      total += 1 + down;
      if (peak >= down) {
        total -= 1;
      }
    }
  }
  return total;
}

console.log(candy([1, 0, 2]));

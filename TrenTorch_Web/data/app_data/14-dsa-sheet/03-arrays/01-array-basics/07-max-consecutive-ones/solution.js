// O(n) time, O(1) space
function maxConsecutiveOnes(nums) {
  let best = 0, current = 0;
  for (const x of nums) {
    if (x === 1) {
      current += 1;
      if (current > best) best = current;
    } else {
      current = 0;
    }
  }
  return best;
}

console.log(maxConsecutiveOnes([1, 1, 0, 1, 1, 1]));

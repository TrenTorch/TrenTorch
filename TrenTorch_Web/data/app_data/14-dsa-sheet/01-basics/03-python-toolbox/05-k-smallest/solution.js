// Average O(n) time, O(n) extra space
function kSmallest(nums, k) {
  if (k <= 0) return [];
  if (k >= nums.length) return nums.slice().sort((a, b) => a - b);
  let chosen = [];
  let pool = nums.slice();
  let need = k;
  while (need > 0) {
    const pivot = pool[Math.floor(Math.random() * pool.length)];
    const less = [];
    const equal = [];
    const greater = [];
    for (let i = 0; i < pool.length; i++) {
      const x = pool[i];
      if (x < pivot) {
        less.push(x);
      } else if (x === pivot) {
        equal.push(x);
      } else {
        greater.push(x);
      }
    }
    if (need <= less.length) {
      pool = less;
    } else if (need <= less.length + equal.length) {
      chosen = chosen.concat(less);
      chosen = chosen.concat(equal.slice(0, need - less.length));
      need = 0;
    } else {
      chosen = chosen.concat(less);
      chosen = chosen.concat(equal);
      need -= less.length + equal.length;
      pool = greater;
    }
  }
  return chosen.sort((a, b) => a - b);
}

console.log(kSmallest([7, 2, 9, 4, 2], 3));

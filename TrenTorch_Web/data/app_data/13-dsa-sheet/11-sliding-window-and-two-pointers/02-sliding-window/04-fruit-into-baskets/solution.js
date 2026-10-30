// O(n) time, O(1) space
function totalFruit(fruits) {
  const count = {};
  let left = 0;
  let best = 0;
  let distinct = 0;
  for (let right = 0; right < fruits.length; right++) {
    const f = fruits[right];
    if (!count[f]) {
      count[f] = 0;
      distinct++;
    }
    count[f]++;
    while (distinct > 2) {
      const leftFruit = fruits[left];
      count[leftFruit]--;
      if (count[leftFruit] === 0) {
        delete count[leftFruit];
        distinct--;
      }
      left++;
    }
    best = Math.max(best, right - left + 1);
  }
  return best;
}

console.log(totalFruit([1, 2, 3, 2, 2]));

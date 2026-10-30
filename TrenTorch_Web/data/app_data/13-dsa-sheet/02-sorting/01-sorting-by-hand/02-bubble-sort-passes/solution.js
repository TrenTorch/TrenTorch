// O(n log n) time, O(n) space
function bubbleSortPasses(nums) {
  const uniq = Array.from(new Set(nums)).sort((a, b) => a - b);
  const rank = new Map();
  uniq.forEach((v, i) => rank.set(v, i + 1));
  const size = uniq.length;
  const tree = new Array(size + 1).fill(0);
  let mostBiggerBefore = 0;
  for (let seen = 0; seen < nums.length; seen++) {
    const x = nums[seen];
    let i = rank.get(x);
    let notBigger = 0;
    while (i > 0) {
      notBigger += tree[i];
      i -= i & -i;
    }
    mostBiggerBefore = Math.max(mostBiggerBefore, seen - notBigger);
    i = rank.get(x);
    while (i <= size) {
      tree[i] += 1;
      i += i & -i;
    }
  }
  return mostBiggerBefore + 1;
}

console.log(bubbleSortPasses([3, 2, 1]));

// O(n * 2^n) time, O(2^n) space
function allSubsetSums(nums) {
  let sums = [0];
  for (const x of nums) {
    const shifted = sums.map(s => s + x);
    const merged = [];
    let i = 0, j = 0;
    while (i < sums.length && j < shifted.length) {
      if (sums[i] <= shifted[j]) {
        merged.push(sums[i++]);
      } else {
        merged.push(shifted[j++]);
      }
    }
    while (i < sums.length) merged.push(sums[i++]);
    while (j < shifted.length) merged.push(shifted[j++]);
    sums = merged;
  }
  return sums;
}

console.log(allSubsetSums([1, 2]));

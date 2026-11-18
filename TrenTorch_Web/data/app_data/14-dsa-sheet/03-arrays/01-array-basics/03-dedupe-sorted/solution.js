// O(n) time, O(n) space
function dedupeSorted(nums) {
  const out = [];
  for (const x of nums) {
    if (out.length === 0 || out[out.length - 1] !== x) {
      out.push(x);
    }
  }
  return out;
}

console.log(dedupeSorted([1, 1, 2, 2, 2, 3]));

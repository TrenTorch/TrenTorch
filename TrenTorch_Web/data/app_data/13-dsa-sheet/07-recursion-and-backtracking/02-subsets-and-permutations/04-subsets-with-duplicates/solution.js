// O(2^n) time, O(n) extra space for recursion stack and current subset
function subsetsWithDuplicates(nums) {
  const a = nums.slice().sort((x, y) => x - y);
  const out = [];
  const current = [];

  function go(start) {
    out.push(current.slice());
    for (let j = start; j < a.length; j++) {
      if (j > start && a[j] === a[j - 1]) continue;
      current.push(a[j]);
      go(j + 1);
      current.pop();
    }
  }

  go(0);
  return out;
}

console.log(subsetsWithDuplicates([1, 2, 2]));

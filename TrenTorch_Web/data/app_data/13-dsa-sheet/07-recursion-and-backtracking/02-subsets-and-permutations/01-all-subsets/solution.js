// O(2^n) time, O(2^n) space
function allSubsets(nums) {
  const a = nums.slice().sort((x, y) => x - y);
  const out = [];

  function go(start, current) {
    out.push(current.slice());
    for (let j = start; j < a.length; j++) {
      current.push(a[j]);
      go(j + 1, current);
      current.pop();
    }
  }

  go(0, []);
  return out;
}

console.log(allSubsets([1, 2, 3]));

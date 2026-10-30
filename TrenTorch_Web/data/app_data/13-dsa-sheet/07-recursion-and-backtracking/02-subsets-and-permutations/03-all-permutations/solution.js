// O(n * n!) time, O(n) auxiliary space (output size excluded)
function allPermutations(nums) {
  const a = nums.slice().sort((x, y) => x - y);
  const used = new Array(a.length).fill(false);
  const out = [];
  const current = [];

  function go() {
    if (current.length === a.length) {
      out.push(current.slice());
      return;
    }
    for (let j = 0; j < a.length; j++) {
      if (used[j]) continue;
      used[j] = true;
      current.push(a[j]);
      go();
      current.pop();
      used[j] = false;
    }
  }

  go();
  return out;
}

console.log(allPermutations([1, 2, 3]));

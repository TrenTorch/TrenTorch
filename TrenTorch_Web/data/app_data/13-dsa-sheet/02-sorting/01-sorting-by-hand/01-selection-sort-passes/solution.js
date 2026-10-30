// O(n^2) time, O(n) space
function selectionSortPasses(nums) {
  const a = nums.slice(); // copy to avoid mutating input
  const passes = [];
  for (let i = 0; i < a.length - 1; i++) {
    let smallest = i;
    for (let j = i + 1; j < a.length; j++) {
      if (a[j] < a[smallest]) {
        smallest = j;
      }
    }
    // swap even if smallest == i
    const temp = a[i];
    a[i] = a[smallest];
    a[smallest] = temp;
    passes.push(a.slice());
  }
  return passes;
}

console.log(selectionSortPasses([64, 25, 12, 22, 11]));

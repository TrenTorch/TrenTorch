// O(n) time, O(1) extra space (excluding the output copy)
function partitionArray(nums) {
  const a = nums.slice(); // copy to avoid mutating input
  const pivot = a[a.length - 1];
  let i = -1;
  for (let j = 0; j < a.length - 1; j++) {
    if (a[j] <= pivot) {
      i++;
      const temp = a[i];
      a[i] = a[j];
      a[j] = temp;
    }
  }
  const pivotPos = i + 1;
  const temp = a[pivotPos];
  a[pivotPos] = a[a.length - 1];
  a[a.length - 1] = temp;
  return [a, pivotPos];
}

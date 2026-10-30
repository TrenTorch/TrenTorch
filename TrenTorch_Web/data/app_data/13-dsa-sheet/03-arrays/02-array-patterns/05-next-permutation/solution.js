function nextPermutation(nums) {
  // O(n) time, O(n) space
  const a = [...nums];
  let i = a.length - 2;
  while (i >= 0 && a[i] >= a[i + 1]) {
    i--;
  }
  if (i >= 0) {
    let j = a.length - 1;
    while (a[j] <= a[i]) {
      j--;
    }
    [a[i], a[j]] = [a[j], a[i]];
  }
  // reverse the suffix from i+1 to end
  let left = i + 1;
  let right = a.length - 1;
  while (left < right) {
    [a[left], a[right]] = [a[right], a[left]];
    left++;
    right--;
  }
  return a;
}

console.log(nextPermutation([1, 2, 3]));

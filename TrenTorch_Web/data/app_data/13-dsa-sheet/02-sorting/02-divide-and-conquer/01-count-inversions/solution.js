// O(n log n) time, O(n) space
function countInversions(nums) {
  function sort(arr) {
    if (arr.length <= 1) {
      return [arr, 0];
    }
    const mid = Math.floor(arr.length / 2);
    const [left, leftInv] = sort(arr.slice(0, mid));
    const [right, rightInv] = sort(arr.slice(mid));
    const merged = [];
    let i = 0,
      j = 0,
      cross = 0;
    while (i < left.length && j < right.length) {
      if (left[i] <= right[j]) {
        merged.push(left[i++]);
      } else {
        merged.push(right[j++]);
        cross += left.length - i;
      }
    }
    if (i < left.length) merged.push(...left.slice(i));
    if (j < right.length) merged.push(...right.slice(j));
    return [merged, leftInv + rightInv + cross];
  }

  return sort(nums)[1];
}

console.log(countInversions([3, 1, 2]));

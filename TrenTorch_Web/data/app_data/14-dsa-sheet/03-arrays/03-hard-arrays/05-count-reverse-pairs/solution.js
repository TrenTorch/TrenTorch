// O(n log n) time, O(n) space
function countReversePairs(nums) {
  function sort(arr) {
    if (arr.length <= 1) {
      return [arr, 0];
    }
    const mid = Math.floor(arr.length / 2);
    const [left, leftCount] = sort(arr.slice(0, mid));
    const [right, rightCount] = sort(arr.slice(mid));
    let count = leftCount + rightCount;
    let j = 0;
    for (let i = 0; i < left.length; i++) {
      while (j < right.length && left[i] > 2 * right[j]) {
        j++;
      }
      count += j;
    }
    // merge left and right
    const merged = [];
    let i = 0;
    j = 0;
    while (i < left.length && j < right.length) {
      if (left[i] <= right[j]) {
        merged.push(left[i++]);
      } else {
        merged.push(right[j++]);
      }
    }
    while (i < left.length) merged.push(left[i++]);
    while (j < right.length) merged.push(right[j++]);
    return [merged, count];
  }
  return sort(nums)[1];
}

console.log(countReversePairs([1, 3, 2, 3, 1]));

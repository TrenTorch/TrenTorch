// O(q log n) time, O(1) extra space
function lowerBound(arr, target) {
  let left = 0, right = arr.length;
  while (left < right) {
    const mid = (left + right) >> 1;
    if (arr[mid] < target) left = mid + 1;
    else right = mid;
  }
  return left;
}

function upperBound(arr, target) {
  let left = 0, right = arr.length;
  while (left < right) {
    const mid = (left + right) >> 1;
    if (arr[mid] <= target) left = mid + 1;
    else right = mid;
  }
  return left;
}

function countInRange(sortedNums, queries) {
  const result = new Array(queries.length);
  for (let i = 0; i < queries.length; i++) {
    const [lo, hi] = queries[i];
    const leftIdx = lowerBound(sortedNums, lo);
    const rightIdx = upperBound(sortedNums, hi);
    result[i] = rightIdx - leftIdx;
  }
  return result;
}

console.log(countInRange([1, 3, 3, 5, 8], [[3, 5], [0, 0], [2, 9]]));

// O(n log n) time, O(n) space
function insertionSortShifts(nums) {
  // Build rank map: value -> 1-based index in sorted unique list
  const uniqueSorted = Array.from(new Set(nums)).sort((a, b) => a - b);
  const rank = new Map();
  for (let i = 0; i < uniqueSorted.length; i++) {
    rank.set(uniqueSorted[i], i + 1);
  }

  const size = uniqueSorted.length;
  const tree = new Array(size + 1).fill(0);
  let shifts = 0;

  for (let seen = 0; seen < nums.length; seen++) {
    const x = nums[seen];
    let i = rank.get(x);

    // query prefix sum: count of elements <= x seen so far
    let notBigger = 0;
    while (i > 0) {
      notBigger += tree[i];
      i -= i & -i;
    }

    shifts += seen - notBigger; // elements greater than x before it

    // update: add current element to BIT
    i = rank.get(x);
    while (i <= size) {
      tree[i] += 1;
      i += i & -i;
    }
  }

  return shifts;
}

console.log(insertionSortShifts([3, 1, 2]));

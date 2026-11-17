// O(n) time, O(n) space
function longestWithinLimit(nums, limit) {
  const big = []; // deque for max values (indices)
  let bigStart = 0;
  const small = []; // deque for min values (indices)
  let smallStart = 0;
  let left = 0;
  let best = 0;

  for (let right = 0; right < nums.length; right++) {
    const x = nums[right];

    while (big.length > bigStart && nums[big[big.length - 1]] <= x) {
      big.pop();
    }
    big.push(right);

    while (small.length > smallStart && nums[small[small.length - 1]] >= x) {
      small.pop();
    }
    small.push(right);

    while (nums[big[bigStart]] - nums[small[smallStart]] > limit) {
      left++;
      if (big[bigStart] < left) bigStart++;
      if (small[smallStart] < left) smallStart++;
    }

    const currentLen = right - left + 1;
    if (currentLen > best) best = currentLen;
  }

  return best;
}

console.log(longestWithinLimit([8, 2, 4, 7], 4));

// O(n) time, O(n) space
function shortestSubarraySumK(nums, k) {
  const n = nums.length;
  const prefix = new Array(n + 1);
  prefix[0] = 0;
  for (let i = 0; i < n; i++) {
    prefix[i + 1] = prefix[i] + nums[i];
  }
  let best = n + 1;
  const window = [];
  let head = 0;

  for (let b = 0; b <= n; b++) {
    const p = prefix[b];
    while (head < window.length && p - prefix[window[head]] >= k) {
      best = Math.min(best, b - window[head]);
      head++;
    }
    while (head < window.length && prefix[window[window.length - 1]] >= p) {
      window.pop();
    }
    window.push(b);
  }
  return best <= n ? best : -1;
}

console.log(shortestSubarraySumK([2, -1, 2], 3));

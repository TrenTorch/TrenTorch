// O(n) time, O(n) space
function sumSubarrayMins(arr) {
  const n = arr.length;
  const left = new Array(n);
  const right = new Array(n);
  const stack = [];
  
  for (let i = 0; i < n; i++) {
    while (stack.length > 0 && arr[stack[stack.length - 1]] >= arr[i]) {
      stack.pop();
    }
    left[i] = stack.length > 0 ? stack[stack.length - 1] : -1;
    stack.push(i);
  }
  
  stack.length = 0;
  
  for (let i = n - 1; i >= 0; i--) {
    while (stack.length > 0 && arr[stack[stack.length - 1]] > arr[i]) {
      stack.pop();
    }
    right[i] = stack.length > 0 ? stack[stack.length - 1] : n;
    stack.push(i);
  }
  
  const MOD = 1000000007;
  let sum = 0;
  for (let i = 0; i < n; i++) {
    const count = (i - left[i]) * (right[i] - i);
    sum = (sum + arr[i] * count) % MOD;
  }
  return sum;
}

console.log(sumSubarrayMins([3, 1, 2, 4]));

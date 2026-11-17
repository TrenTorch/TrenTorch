// O(n) time, O(n) space
function removeKDigits(num, k) {
  const stack = [];
  for (let i = 0; i < num.length; i++) {
    const ch = num[i];
    while (k > 0 && stack.length && stack[stack.length - 1] > ch) {
      stack.pop();
      k--;
    }
    stack.push(ch);
  }
  if (k > 0) {
    stack.length = stack.length - k;
  }
  let result = stack.join('').replace(/^0+/, '');
  if (result === '') result = '0';
  return result;
}

console.log(removeKDigits("1432219", 3));

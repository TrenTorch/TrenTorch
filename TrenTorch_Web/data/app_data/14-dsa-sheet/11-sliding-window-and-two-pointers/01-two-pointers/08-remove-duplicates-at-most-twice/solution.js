// O(n) time, O(n) space
function keepAtMostTwice(nums) {
  const a = [...nums];
  let write = 0;
  for (let read = 0; read < a.length; read++) {
    if (write < 2 || a[read] !== a[write - 2]) {
      a[write] = a[read];
      write++;
    }
  }
  return a.slice(0, write);
}

console.log(keepAtMostTwice([1, 1, 1, 2, 2, 3]));

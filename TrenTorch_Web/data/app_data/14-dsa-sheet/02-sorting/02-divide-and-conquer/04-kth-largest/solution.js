// Expected O(n) average time, O(n) extra space
function kthLargest(nums, k) {
  let a = nums.slice(); // make a copy
  let target = a.length - k;
  while (true) {
    const pivot = a[Math.floor(Math.random() * a.length)];
    const less = [];
    let equalCount = 0;
    for (let i = 0; i < a.length; i++) {
      const x = a[i];
      if (x < pivot) {
        less.push(x);
      } else if (x === pivot) {
        equalCount++;
      }
    }
    if (target < less.length) {
      a = less;
    } else if (target < less.length + equalCount) {
      return pivot;
    } else {
      target -= less.length + equalCount;
      const greater = [];
      for (let i = 0; i < a.length; i++) {
        const x = a[i];
        if (x > pivot) {
          greater.push(x);
        }
      }
      a = greater;
    }
  }
}

console.log(kthLargest([3, 2, 1, 5, 6, 4], 2));

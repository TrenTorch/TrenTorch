function robCircle(nums) {
  // O(n) time, O(n) space
  const line = (houses) => {
    let skip = 0, take = 0;
    for (const x of houses) {
      const newSkip = Math.max(skip, take);
      take = skip + x;
      skip = newSkip;
    }
    return Math.max(skip, take);
  };

  if (nums.length === 1) {
    return nums[0];
  }
  return Math.max(line(nums.slice(1)), line(nums.slice(0, -1)));
}

console.log(robCircle([2, 3, 2]));

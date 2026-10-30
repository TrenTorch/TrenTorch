package main

import "fmt"

// O(n) time, O(1) space (Kadane's algorithm)
func maxSubarraySum(nums []int) int {
	best := nums[0]
	cur := nums[0]
	for _, x := range nums[1:] {
		cur = max(x, cur+x)
		best = max(best, cur)
	}
	return best
}

func main() {
	fmt.Println(maxSubarraySum([]int{-2, 1, -3, 4, -1, 2, 1, -5, 4}))
}

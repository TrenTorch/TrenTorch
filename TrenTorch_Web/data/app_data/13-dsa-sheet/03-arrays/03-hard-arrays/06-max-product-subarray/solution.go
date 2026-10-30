package main

import "fmt"

// O(n) time, O(1) space
func maxProductSubarray(nums []int) int {
	best := nums[0]
	hi, lo := nums[0], nums[0]
	for _, x := range nums[1:] {
		a, b, c := x, hi*x, lo*x
		hi = max(a, b, c)
		lo = min(a, b, c)
		best = max(best, hi)
	}
	return best
}

func main() {
	fmt.Println(maxProductSubarray([]int{2, 3, -2, 4}))
}

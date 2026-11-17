package main

import "fmt"

// O(n) time, O(1) space
func maxSubarrayRange(nums []int) []int {
	bestSum, bestStart, bestEnd := nums[0], 0, 0
	current := nums[0]
	begin := 0
	for i := 1; i < len(nums); i++ {
		if current < 0 {
			current = nums[i]
			begin = i
		} else {
			current += nums[i]
		}
		if current > bestSum {
			bestSum, bestStart, bestEnd = current, begin, i
		}
	}
	return []int{bestSum, bestStart, bestEnd}
}

func main() {
	fmt.Println(maxSubarrayRange([]int{-2, 1, -3, 4, -1, 2, 1, -5, 4}))
}

package main

import "fmt"

// O(n) time, O(1) space
func maxSumK(nums []int, k int) int {
	total := 0
	for i := 0; i < k; i++ {
		total += nums[i]
	}
	best := total
	for i := k; i < len(nums); i++ {
		total += nums[i] - nums[i-k]
		if total > best {
			best = total
		}
	}
	return best
}

func main() {
	fmt.Println(maxSumK([]int{2, 1, 5, 1, 3, 2}, 3))
}

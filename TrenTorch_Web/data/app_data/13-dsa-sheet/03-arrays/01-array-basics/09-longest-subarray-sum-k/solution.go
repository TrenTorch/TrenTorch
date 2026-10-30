package main

import "fmt"

// O(n) time, O(1) space
func longestSubarraySumK(nums []int, k int) int {
	best, left, total := 0, 0, 0
	for right, x := range nums {
		total += x
		for total > k && left <= right {
			total -= nums[left]
			left++
		}
		if total == k {
			best = max(best, right-left+1)
		}
	}
	return best
}

func main() {
	fmt.Println(longestSubarraySumK([]int{1, 2, 3, 1, 1, 1, 1}, 3))
}

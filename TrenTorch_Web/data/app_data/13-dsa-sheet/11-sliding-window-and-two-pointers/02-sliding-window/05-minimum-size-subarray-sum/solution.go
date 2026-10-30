package main

import "fmt"

// O(n) time, O(1) space
func minSubarrayLen(target int, nums []int) int {
	best := len(nums) + 1
	total := 0
	left := 0
	for right, x := range nums {
		total += x
		for total >= target {
			if right-left+1 < best {
				best = right - left + 1
			}
			total -= nums[left]
			left++
		}
	}
	if best <= len(nums) {
		return best
	}
	return 0
}

func main() {
	fmt.Println(minSubarrayLen(7, []int{2, 3, 1, 2, 4, 3}))
}

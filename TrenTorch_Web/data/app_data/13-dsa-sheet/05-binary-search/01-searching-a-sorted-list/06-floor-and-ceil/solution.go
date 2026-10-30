package main

import "fmt"

// O(log n) time, O(1) space
func floorAndCeil(nums []int, target int) []int {
	lo, hi := 0, len(nums)
	for lo < hi {
		mid := lo + (hi-lo)/2
		if nums[mid] < target {
			lo = mid + 1
		} else {
			hi = mid
		}
	}

	ceil := -1
	if lo < len(nums) {
		ceil = nums[lo]
	}

	floor := -1
	if lo < len(nums) && nums[lo] == target {
		floor = target
	} else if lo > 0 {
		floor = nums[lo-1]
	}
	return []int{floor, ceil}
}

func main() {
	fmt.Println(floorAndCeil([]int{1, 2, 8, 10, 11, 12, 19}, 5))
}

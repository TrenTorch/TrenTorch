package main

import "fmt"

// O(log n) time, O(1) space
func lowerBound(nums []int, target int) int {
	lo, hi := 0, len(nums)
	for lo < hi {
		mid := lo + (hi-lo)/2
		if nums[mid] < target {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	return lo
}

func main() {
	fmt.Println(lowerBound([]int{1, 2, 2, 2, 5}, 2))
}

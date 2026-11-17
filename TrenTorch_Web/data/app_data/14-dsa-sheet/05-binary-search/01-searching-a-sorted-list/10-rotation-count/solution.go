package main

import "fmt"

// O(log n) time, O(1) space
func rotationCount(nums []int) int {
	lo, hi := 0, len(nums)-1
	for lo < hi {
		mid := lo + (hi-lo)/2
		if nums[mid] > nums[hi] {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	return lo
}

func main() {
	fmt.Println(rotationCount([]int{3, 4, 5, 1, 2}))
}

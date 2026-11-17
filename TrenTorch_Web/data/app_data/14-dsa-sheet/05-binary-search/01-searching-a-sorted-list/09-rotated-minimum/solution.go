package main

import "fmt"

// O(log n) time, O(1) space
func rotatedMinimum(nums []int) int {
	lo, hi := 0, len(nums)-1
	for lo < hi {
		mid := lo + (hi-lo)/2
		if nums[mid] > nums[hi] {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	return nums[lo]
}

func main() {
	fmt.Println(rotatedMinimum([]int{4, 5, 6, 7, 0, 1, 2}))
}

package main

import "fmt"

// O(log n) time, O(1) space
func mountainPeak(nums []int) int {
	lo, hi := 0, len(nums)-1
	for lo < hi {
		mid := lo + (hi-lo)/2
		if nums[mid] < nums[mid+1] {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	return lo
}

func main() {
	fmt.Println(mountainPeak([]int{1, 3, 5, 4, 2}))
}

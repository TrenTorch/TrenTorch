package main

import "fmt"

// O(log n) time, O(1) space
func singleNonDuplicate(nums []int) int {
	lo, hi := 0, len(nums)-1
	for lo < hi {
		mid := lo + (hi-lo)/2
		if mid%2 == 1 {
			mid--
		}
		if nums[mid] == nums[mid+1] {
			lo = mid + 2
		} else {
			hi = mid
		}
	}
	return nums[lo]
}

func main() {
	fmt.Println(singleNonDuplicate([]int{1, 1, 2, 3, 3, 4, 4, 8, 8}))
}

package main

import "fmt"

// O(log n) time, O(1) space
func binarySearchIndex(nums []int, target int) int {
	lo, hi := 0, len(nums)-1
	for lo <= hi {
		mid := lo + (hi-lo)/2
		if nums[mid] == target {
			return mid
		}
		if nums[mid] < target {
			lo = mid + 1
		} else {
			hi = mid - 1
		}
	}
	return -1
}

func main() {
	fmt.Println(binarySearchIndex([]int{-1, 0, 3, 5, 9, 12}, 9))
}

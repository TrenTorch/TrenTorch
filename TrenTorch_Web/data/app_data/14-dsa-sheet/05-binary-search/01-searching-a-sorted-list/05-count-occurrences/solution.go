package main

import "fmt"

// bisectLeft returns the first index i with nums[i] >= target.
func bisectLeft(nums []int, target int) int {
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

// bisectRight returns the first index i with nums[i] > target.
func bisectRight(nums []int, target int) int {
	lo, hi := 0, len(nums)
	for lo < hi {
		mid := lo + (hi-lo)/2
		if nums[mid] <= target {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	return lo
}

// O(log n) time, O(1) space
func countOccurrences(nums []int, target int) int {
	return bisectRight(nums, target) - bisectLeft(nums, target)
}

func main() {
	fmt.Println(countOccurrences([]int{1, 2, 2, 2, 3}, 2))
}

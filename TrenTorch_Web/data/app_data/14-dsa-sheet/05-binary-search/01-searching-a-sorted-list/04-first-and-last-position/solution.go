package main

import "fmt"

// O(log n) time, O(1) space
func firstAndLast(nums []int, target int) []int {
	lo, hi := 0, len(nums)
	for lo < hi {
		mid := lo + (hi-lo)/2
		if nums[mid] < target {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	if lo == len(nums) || nums[lo] != target {
		return []int{-1, -1}
	}
	first := lo

	hi = len(nums)
	for lo < hi {
		mid := lo + (hi-lo)/2
		if nums[mid] <= target {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	return []int{first, lo - 1}
}

func main() {
	fmt.Println(firstAndLast([]int{5, 7, 7, 8, 8, 10}, 8))
}

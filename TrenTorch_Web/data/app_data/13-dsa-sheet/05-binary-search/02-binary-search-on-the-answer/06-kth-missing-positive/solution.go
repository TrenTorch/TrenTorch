package main

import "fmt"

// O(log n) time, O(1) space
func kthMissingPositive(nums []int, k int) int {
	lo, hi := 0, len(nums)
	for lo < hi {
		mid := (lo + hi) / 2
		if nums[mid]-(mid+1) < k {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	return lo + k
}

func main() {
	fmt.Println(kthMissingPositive([]int{2, 3, 4, 7, 11}, 5))
}

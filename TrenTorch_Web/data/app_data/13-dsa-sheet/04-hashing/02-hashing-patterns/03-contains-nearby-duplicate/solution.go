package main

import "fmt"

// O(n) time, O(k) space (sliding window of the last k values)
func containsNearbyDuplicate(nums []int, k int) bool {
	window := map[int]bool{}
	for i, x := range nums {
		if window[x] {
			return true
		}
		window[x] = true
		if i >= k {
			delete(window, nums[i-k])
		}
	}
	return false
}

func main() {
	fmt.Println(containsNearbyDuplicate([]int{1, 2, 3, 1}, 3))
}

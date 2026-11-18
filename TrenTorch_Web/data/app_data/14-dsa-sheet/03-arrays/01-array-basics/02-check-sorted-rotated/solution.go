package main

import "fmt"

// O(n) time, O(1) space (count descents around the circle; at most one is allowed).
func checkSortedRotated(nums []int) bool {
	n := len(nums)
	drops := 0
	for i := 0; i < n; i++ {
		if nums[i] > nums[(i+1)%n] {
			drops++
		}
	}
	return drops <= 1
}

func main() {
	fmt.Println(checkSortedRotated([]int{3, 4, 5, 1, 2}))
}

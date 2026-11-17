package main

import "fmt"

// O(n) time, O(1) space
func pivotIndex(nums []int) int {
	total := 0
	for _, x := range nums {
		total += x
	}
	left := 0
	for i, x := range nums {
		if left == total-left-x {
			return i
		}
		left += x
	}
	return -1
}

func main() {
	fmt.Println(pivotIndex([]int{1, 7, 3, 6, 5, 6}))
}

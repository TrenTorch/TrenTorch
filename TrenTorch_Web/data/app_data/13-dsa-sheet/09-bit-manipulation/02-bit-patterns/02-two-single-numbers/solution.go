package main

import "fmt"

// O(n) time, O(1) space
func twoSingleNumbers(nums []int) []int {
	xorAll := 0
	for _, x := range nums {
		xorAll ^= x
	}
	low := xorAll & -xorAll
	a, b := 0, 0
	for _, x := range nums {
		if x&low != 0 {
			a ^= x
		} else {
			b ^= x
		}
	}
	if a > b {
		a, b = b, a
	}
	return []int{a, b}
}

func main() {
	fmt.Println(twoSingleNumbers([]int{1, 2, 1, 3, 2, 5}))
}

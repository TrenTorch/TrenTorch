package main

import "fmt"

// O(n) time, O(1) space
func singleNumber(nums []int) int {
	result := 0
	for _, x := range nums {
		result ^= x
	}
	return result
}

func main() {
	fmt.Println(singleNumber([]int{4, 1, 2, 1, 2}))
}

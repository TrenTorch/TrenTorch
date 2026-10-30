package main

import "fmt"

// O(n) time, O(1) space
func missingNumber(nums []int) int {
	n := len(nums)
	total := 0
	for _, x := range nums {
		total += x
	}
	return n*(n+1)/2 - total
}

func main() {
	fmt.Println(missingNumber([]int{3, 0, 1}))
}

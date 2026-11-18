package main

import "fmt"

// O(n) time, O(n) space
func longestZeroSumSubarray(nums []int) int {
	first := map[int]int{0: -1}
	prefix, best := 0, 0
	for i, x := range nums {
		prefix += x
		if j, ok := first[prefix]; ok {
			best = max(best, i-j)
		} else {
			first[prefix] = i
		}
	}
	return best
}

func main() {
	fmt.Println(longestZeroSumSubarray([]int{15, -2, 2, -8, 1, 7, 10, 23}))
}
